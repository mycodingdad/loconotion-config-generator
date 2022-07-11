from modules.generator import Generator
from unittest import TestCase

def test_merge_config():
    generated_config_dict = { "key1" : 1, "key2" : 2, "key3" : { "key3-1" : 31, "key3-2" : 32}}
    merge_config_dict = { "key2" : 22, "key3" : { "key3-3" : 33} }

    generator = Generator({}, {})
    merged_config_dict = generator.merge_config_dict(generated_config_dict, merge_config_dict)

    expected_config_dict = { "key1" : 1, "key2" : 22, "key3" : { "key3-1" : 31, "key3-2" : 32, "key3-3" : 33}}

    test_case = TestCase()
    test_case.maxDiff = 99999
    test_case.assertDictEqual( expected_config_dict, merged_config_dict)



def test_create_config():
    page_info_dict = {
        "59f6278a93e04df09e80b20b9d2a3bca":{
            "slug":"404",
            "title":"페이지를 찾을 수가 없어요",
            "description":""
        },
        "b69aacb4f2b7415497ef90dccfa76e64":{
            "slug":"2022-06-28-blog-migration-loconotion",
            "title":"loconotion과 Notion으로 블로그 이전",
            "description":"워드프레스에서 운영하던 블로그를 notablog와 loconotion으로 이전한 이야기. 그리고 리다이렉트와 사이트맵 만들기."
        },
    }

    meta_config = {
        "site_title" : "CodingDad 2.0; No Secret Wiki",
        "site_description" : "I'm a programmer who likes to make games with my son.",
        "site_url" : "https://codingdad.me",
        "site_image" : "https://codingdad.me/codingdad_logo.png",
        "twitter_site" : "@mycodingdad",
        "twitter_creator" : "@mycodingdad",
    }

    expected_config = {
        "site" : {
            "meta" : [
                {"name" : "title",  "content" : "CodingDad 2.0; No Secret Wiki"},
                {"name" : "description",  "content" : "I'm a programmer who likes to make games with my son."},
                {"property" : "og:site_name",  "content" : "CodingDad 2.0; No Secret Wiki"},
                {"property" : "og:type",  "content" : "Website"},
                {"property" : "og:title",  "content" : "CodingDad 2.0; No Secret Wiki"},
                {"property" : "og:description",  "content" : "I'm a programmer who likes to make games with my son."},
                {"property" : "og:image",  "content" : "https://codingdad.me/codingdad_logo.png"},
                {"property" : "og:url",  "content" : "https://codingdad.me"},
                {"name" : "twitter:card",  "content" : "summary"},
                {"name" : "twitter:site",  "content" : "@mycodingdad"},
                {"name" : "twitter:creator",  "content" : "@mycodingdad"},
                {"name" : "twitter:title",  "content" : "CodingDad 2.0; No Secret Wiki"},
                {"name" : "twitter:description",  "content" : "I'm a programmer who likes to make games with my son."},
                {"name" : "twitter:image",  "content" : "https://codingdad.me/codingdad_logo.png"},
                {"name" : "twitter:url",  "content" : "https://codingdad.me"},
            ]
        },
        "pages" : {
            "59f6278a93e04df09e80b20b9d2a3bca":{
                "slug" : "404",
                "meta" : [
                    {"name" : "title",  "content" : "페이지를 찾을 수가 없어요"},
                    {"name" : "description",  "content" : ""},
                    {"property" : "og:site_name",  "content" : "페이지를 찾을 수가 없어요"},
                    {"property" : "og:type",  "content" : "Website"},
                    {"property" : "og:title",  "content" : "페이지를 찾을 수가 없어요"},
                    {"property" : "og:description",  "content" : ""},
                    {"property" : "og:image",  "content" : "https://codingdad.me/codingdad_logo.png"},
                    {"property" : "og:url",  "content" : "https://codingdad.me/404.html"},
                    {"name" : "twitter:card",  "content" : "summary"},
                    {"name" : "twitter:site",  "content" : "@mycodingdad"},
                    {"name" : "twitter:creator",  "content" : "@mycodingdad"},
                    {"name" : "twitter:title",  "content" : "페이지를 찾을 수가 없어요"},
                    {"name" : "twitter:description",  "content" : ""},
                    {"name" : "twitter:image",  "content" : "https://codingdad.me/codingdad_logo.png"},
                    {"name" : "twitter:url",  "content" : "https://codingdad.me/404.html"},
                ]
            },
            "b69aacb4f2b7415497ef90dccfa76e64":{
                "slug" : "2022-06-28-blog-migration-loconotion",
                "meta" : [
                    {"name" : "title",  "content" : "loconotion과 Notion으로 블로그 이전"},
                    {"name" : "description",  "content" : "워드프레스에서 운영하던 블로그를 notablog와 loconotion으로 이전한 이야기. 그리고 리다이렉트와 사이트맵 만들기."},
                    {"property" : "og:site_name",  "content" : "loconotion과 Notion으로 블로그 이전"},
                    {"property" : "og:type",  "content" : "Website"},
                    {"property" : "og:title",  "content" : "loconotion과 Notion으로 블로그 이전"},
                    {"property" : "og:description",  "content" : "워드프레스에서 운영하던 블로그를 notablog와 loconotion으로 이전한 이야기. 그리고 리다이렉트와 사이트맵 만들기."},
                    {"property" : "og:image",  "content" : "https://codingdad.me/codingdad_logo.png"},
                    {"property" : "og:url",  "content" : "https://codingdad.me/2022-06-28-blog-migration-loconotion.html"},
                    {"name" : "twitter:card",  "content" : "summary"},
                    {"name" : "twitter:site",  "content" : "@mycodingdad"},
                    {"name" : "twitter:creator",  "content" : "@mycodingdad"},
                    {"name" : "twitter:title",  "content" : "loconotion과 Notion으로 블로그 이전"},
                    {"name" : "twitter:description",  "content" : "워드프레스에서 운영하던 블로그를 notablog와 loconotion으로 이전한 이야기. 그리고 리다이렉트와 사이트맵 만들기."},
                    {"name" : "twitter:image",  "content" : "https://codingdad.me/codingdad_logo.png"},
                    {"name" : "twitter:url",  "content" : "https://codingdad.me/2022-06-28-blog-migration-loconotion.html"},
                ]
            }
        }
    }

    generator = Generator(meta_config, {})
    config = generator.create_config_dict(page_info_dict)

    test_case = TestCase()
    test_case.maxDiff = 99999
    test_case.assertDictEqual( expected_config, config)