# Loconotion Config Generator

**Loconotion Config Generator** is a Python script that load a [Notion.so](https://notion.so) database's pages information and generates a [Loconotion](https://github.com/leoncvlt/loconotion) configuration file for changing page URLs and inserting [Open Graph](https://ogp.me/) tags. 

![Architecture](https://raw.githubusercontent.com/mycodingdad/loconotion-config-generator/main/docs/Architecture.svg))

## But Why?

It it cumbersome to fill a Loconotion configuration file with the URL slugs and the meta tags for lots of pages.

## Demo

You can check out an example site built with Loconotion Config Generator: https://codingdad.me

## Installation & Requirements

Make sure you're in your virtual environment of choice, then run
- `pip install -r requirements.txt`

## Usage

You can fully configure Loconotion Config Generator to your needs by passing a [.toml](https://github.com/toml-lang/toml) meta configuration file to the script:

`python loconotion-config-generator example/example_meta_config.toml`

Here's what a full .toml meta configuration would look like, alongside with explanations of each parameter.

```toml
# Path for the generated config 
generated_config_path = "dist/generated_config.toml"

# Path for the config to be merged into the generated config
merge_config_path = "manual_config.toml"


# Notion Database Infomation
database_id = "<Notion Database ID Here>"

# Notion API Configuration
token = "<Notion API Token Here>"

# Notion Database Property names
title_property = "title"
description_property = "description"
slug_property = "slug"
date_property = "date"

# Site Information
site_title = "CodingDad 2.0; No Secret Wiki"
site_description = "I'm a programmer who likes to make games with my son."
site_url = "https://codingdad.me"
site_image = "https://codingdad.me/codingdad_logo.png"

# Twitter Information
twitter_site = "@mycodingdad"
twitter_creator = "@mycodingdad"
```

On top of this, the script can take these optional arguments:

```
  -h, --help        show this help message and exit
  -v, --verbose     Increase output log verbosity
```

## Roadmap / Features wishlist

- [ ] Per-page Open Graph image

## Sites built with Loconotion Config Generator

- [codingdad.me](https://codingdad.me)

If you used Loconotion Config Generator to build a cool site and want it added to the list above, shoot me a mail or submit a pull request!

## Support [![Buy me a coffee](https://img.shields.io/badge/-buy%20me%20a%20coffee-lightgrey?style=flat&logo=buy-me-a-coffee&color=FF813F&logoColor=white "Buy me a coffee")](https://www.buymeacoffee.com/codingdad)

If you found this useful, consider [buying me a coffee](https://www.buymeacoffee.com/codingdad) so I get a a nice dose of methilxanthine, and you get a nice dose of karma.
