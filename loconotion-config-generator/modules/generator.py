from genericpath import exists
import sys
import logging
import json
import os
import codecs
import pprint

log = logging.getLogger(f"loconotion-config-generator.{__name__}")

try:
    import requests
    import toml

except ModuleNotFoundError as e:
    log.critical(f'ModuleNotFoundError: {e}. have you installed the requirements?')
    sys.exit(1)


class Generator:
    def __init__(self, meta_config={}, args={}):
        self.meta_config = meta_config
        self.args = args
    
    def generate(self):
        page_info_dict = self.create_page_info_dict()
        generated_config_dict = self.create_config_dict( page_info_dict)
        merge_config_dict = self.load_merge_config_dict()
        merged_dict = self.merge_config_dict(generated_config_dict, merge_config_dict)
        self.write_config(merged_dict)

    def create_page_info_dict(self):

        database_page_dict = self.get_database_from_notion()

        title_property = self.meta_config.get("title_property")
        description_property = self.meta_config.get("description_property")
        slug_property = self.meta_config.get("slug_property")
        date_property = self.meta_config.get("date_property")

        page_info_dict = {}
        for page in database_page_dict['results']:
            id = page['id'].replace("-", "")
            try:
                # slug
                slug_array = page['properties'][slug_property]['rich_text']
                if len(slug_array) == 0:
                    continue
                slug = slug_array[0]['text']['content']
                date_dict = page['properties'][date_property]['date']
                if date_dict:
                    date = date_dict['start']
                    if date:
                        slug = f'{date}-{slug}'
                # title
                title = page['properties'][title_property]['title'][0]['plain_text']

                # description
                description = ''
                description_array = page['properties'][description_property]['rich_text']
                if len(description_array) > 0:
                    description = description_array[0]['text']['content']
            except Exception as e:
                log.error(f'Exception in getting page info. id:{id}, error:{e}')
                continue

            page_info_dict[id] = {'slug': slug, 'title': title, 'description': description }

        log.debug ( f'page_info_dict = {pprint.pformat(page_info_dict)}')
        return page_info_dict

    def get_database_from_notion(self):
        database_id = self.meta_config.get("database_id", None)
        token = self.meta_config.get("token", None)
        url = f'https://api.notion.com/v1/databases/{database_id}/query'
        headers = {
            "Authorization" : f"Bearer {token}",
            "Notion-Version": "2021-08-16"
        }

        log.debug( f'Notion API Request. url = {url}, headers = {headers}')

        r = requests.post(url, headers=headers)
        database_page_dict = r.json()

        log.debug( f'Notion API Response = {pprint.pformat(database_page_dict)}')
        return database_page_dict

    def create_config_dict( self, page_info_dict):
        site_title = self.meta_config.get("site_title", None)
        site_description = self.meta_config.get("site_description", None)
        site_url = self.meta_config.get("site_url", None)
        site_image = self.meta_config.get("site_image", None)
        twitter_site = self.meta_config.get("twitter_site", None)
        twitter_creator = self.meta_config.get("twitter_creator", None)

        config = {}

        # site
        config["site"] = {}
        config["site"]["meta"] = self.create_meta_array( 
            site_title, 
            site_description, 
            site_image, 
            site_url, 
            twitter_site, 
            twitter_creator
        )

        # pages
        pages = {}
        config["pages"] = pages

        for page_id in page_info_dict:
            page_info = page_info_dict[page_id]
            config["pages"][page_id] = {}

            log.debug ( f'[create_config_dict] page_id={page_id}, page_info={pprint.pformat(page_info)}')

            if page_info["slug"]:
                config["pages"][page_id]["slug"] = page_info["slug"]
            config["pages"][page_id]["meta"] = self.create_meta_array(
                page_info["title"], 
                page_info["description"], 
                site_image,                 #todo: page image
                site_url + '/' + page_info["slug"] + ".html",      #todo: trim slash
                twitter_site, 
                twitter_creator
            )
        
        log.debug( f'generated_config_dict = {json.dumps(config, indent=4)}')
        return config

    def load_merge_config_dict(self):
        merge_config_path = self.meta_config.get("merge_config_path")

        if not os.path.exists(merge_config_path):
            raise f'merge_config_path not exists. path:{merge_config_path}'

        with open(merge_config_path) as f:
            merge_config_string = f.read()
        merge_config_dict = toml.loads(merge_config_string)

        log.debug( f'loaded merge_config_dict = {json.dumps(merge_config_dict, indent=4)}')

        return merge_config_dict

    def merge_config_dict(self, generated_config_dict, merge_config_dict):
        self.merge_dict(generated_config_dict, merge_config_dict)
        log.debug( f'merged config_dict = {json.dumps(generated_config_dict, indent=4)}')
        return generated_config_dict

    def merge_dict(self, dct, merge_dct):
        for k, v in merge_dct.items():
            if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], dict)):
                self.merge_dict(dct[k], merge_dct[k])
            else:
                dct[k] = merge_dct[k]

    def write_config(self, config_dict):
        generated_config_path = self.meta_config.get("generated_config_path")

        config_dir = os.path.dirname(generated_config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        with codecs.open(generated_config_path, "w", "utf-8") as f:
            toml.dump( config_dict, f)

    def create_meta_array( self, title, description, image, url, twitter_site, twitter_creator):
        meta_array = []
        self.add_meta_with_name( meta_array, "title", title)
        self.add_meta_with_name( meta_array, "description", description)
        self.add_meta_with_property( meta_array, "og:site_name", title)
        self.add_meta_with_property( meta_array, "og:type", "Website")
        self.add_meta_with_property( meta_array, "og:title", title)
        self.add_meta_with_property( meta_array, "og:description", description)
        self.add_meta_with_property( meta_array, "og:image", image)
        self.add_meta_with_property( meta_array, "og:url", url)
        self.add_meta_with_name( meta_array, "twitter:card", "summary")
        self.add_meta_with_name( meta_array, "twitter:site", twitter_site)
        self.add_meta_with_name( meta_array, "twitter:creator", twitter_creator)
        self.add_meta_with_name( meta_array, "twitter:title", title)
        self.add_meta_with_name( meta_array, "twitter:description", description)
        self.add_meta_with_name( meta_array, "twitter:image", image)
        self.add_meta_with_name( meta_array, "twitter:url", url)
        return meta_array

    def add_meta_with_name( self, meta_array, name, content):
        meta_array.append( {
            "name": name,
            "content": content
        })

    def add_meta_with_property( self, meta_array, property, content):
        meta_array.append( {
            "property": property,
            "content": content
        })

