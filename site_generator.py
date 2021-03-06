import argparse
import os
import json
import jinja2
import urllib
from copy import deepcopy

from markdown import markdown


TEMPLATES_DIRECTORY = 'templates/'
ARTICLES_DIRECTORY = 'articles/'
SITE_DIRECTORY = 'docs/'

INDEX_FILENAME = 'index.html'
ARTICLE_FILENAME = 'article.html'
CONFIG_FILENAME = 'config.json'


def read_config(config_location):
    with open(config_location, 'r') as config_file:
        return json.load(config_file)

def read_file(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def save_file(content, output_location):
    with open(output_location, 'w') as file:
        file.write(content)

def change_file_extension(file_location, to_ext):
    filepath, _ = os.path.splitext(file_location)
    return '{}.{}'.format(filepath, to_ext)

def get_dir(filepath):
    return os.path.split(filepath)[0]

def get_articles_with_correct_location(articles):
    html_articles = deepcopy(articles)
    for a in html_articles:
        a['source'] = change_file_extension(a['source'], 'html')
    return html_articles

def get_article_output_location(site_directory, article_location):
    location = os.path.join(site_directory, article_location)
    return change_file_extension(location, 'html')

def convert_md_article_to_html(j_template, md_content, a_topic, a_title):
    extensions = ['codehilite', 'fenced_code']
    html = markdown(md_content, extensions=extensions)
    return j_template.render({'html': html,
                            'topic': a_topic,
                            'title': a_title})

def is_html_up_to_date(html_location, source_location):
    return os.path.getmtime(html_location) > os.path.getmtime(source_location)

def create_index(index_template_location, index_result_location,config,
                 only_outdated=False):
    if only_outdated \
    and os.path.exists(index_result_location) \
    and is_html_up_to_date(index_result_location, index_template_location):
        return
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'), autoescape=True)
    index_template = env.get_template(index_template_location)
    articles = get_articles_with_correct_location(config['articles'])
    index_html = index_template.render(topics=config['topics'], articles=articles)
    save_file(index_html, index_result_location)

def create_articles(article_template_location, articles_dir_location, site_dir, config,
                    only_outdated=False):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./') , autoescape=True)
    article_template = env.get_template(article_template_location)
    for article in config['articles']:
        a_location = article['source']
        html_output_location = get_article_output_location(site_dir, a_location)
        article_output_dir = get_dir(html_output_location)
        if not os.path.exists(article_output_dir): os.mkdir(article_output_dir)
        md_source_location = os.path.join(articles_dir_location, a_location)

        if only_outdated \
        and os.path.exists(html_output_location) \
        and is_html_up_to_date(html_output_location, md_source_location) \
        and is_html_up_to_date(html_output_location, article_template_location):
            continue
        article_md_content = read_file(md_source_location)
        html_article = convert_md_article_to_html(article_template,
                                                  article_md_content,
                                                  article['topic'],
                                                  article['title'])
        save_file(html_article, html_output_location)

def get_light_assembly_flag():
    parser = argparse.ArgumentParser(description='Create site with devman articles')
    parser.add_argument('-light', action='store_true', help='Cause script to overwrite only outdated files')
    return parser.parse_args().light

def main():
    light_assembly_flag = get_light_assembly_flag()
    config = read_config(CONFIG_FILENAME)
    article_template_location = os.path.join(TEMPLATES_DIRECTORY, ARTICLE_FILENAME)
    index_template_location = os.path.join(TEMPLATES_DIRECTORY, INDEX_FILENAME)
    index_result_location = os.path.join(SITE_DIRECTORY, INDEX_FILENAME)

    if not os.path.exists(SITE_DIRECTORY): os.mkdir(SITE_DIRECTORY)
    create_index(index_template_location,
                 index_result_location,
                 config,
                 only_outdated=light_assembly_flag)
    create_articles(article_template_location,
                    ARTICLES_DIRECTORY,
                    SITE_DIRECTORY,
                    config,
                    only_outdated=light_assembly_flag)


if __name__ == '__main__':
    main()