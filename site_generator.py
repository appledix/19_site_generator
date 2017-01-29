import os
import json
import jinja2
from copy import deepcopy

from markdown import markdown


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

def get_articles_with_html_location(articles):
    html_articles = deepcopy(articles)
    for a in html_articles:
        a['source'] = change_file_extension(a['source'], 'html')
    return html_articles

def get_article_output_location(site_directory, article_location):
    location = '{}/{}'.format(site_directory, article_location)
    return change_file_extension(location, 'html')

def convert_md_article_to_html(j_template, md_content, a_topic, a_title):
    extensions = ['codehilite', 'fenced_code']
    html = markdown(md_content, extensions=extensions)
    return j_template.render({'html': html,
                            'topic': a_topic,
                            'title': a_title})

def create_index(index_template_location, index_result_location, config):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./'), autoescape=True)
    index_template = env.get_template(index_template_location)
    articles = get_articles_with_html_location(config['articles'])
    index_html = index_template.render(topics=config['topics'], articles=articles)
    save_file(index_html, index_result_location)

def is_html_up_to_date(html_location, source_location):
    return os.path.getmtime(html_location) > os.path.getmtime(source_location)

def create_articles(article_template_location, articles_dir_location, site_dir, config):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('./') , autoescape=True)
    article_template = env.get_template(article_template_location)
    for article in config['articles']:
        a_location = article['source']
        html_output_location = get_article_output_location(site_dir, a_location)
        article_output_dir = get_dir(html_output_location)
        if not os.path.exists(article_output_dir): os.mkdir(article_output_dir)
        md_source_location = '{}{}'.format(articles_dir_location, a_location)
        if os.path.exists(html_output_location) \
        and is_html_up_to_date(html_output_location, md_source_location):
            continue
        article_md_content = read_file(md_source_location)
        html_article = convert_md_article_to_html(article_template,
                                                  article_md_content,
                                                  article['topic'],
                                                  article['title'])
        save_file(html_article, html_output_location)

def main():
    config = read_config('config.json')
    articles_dir_location = 'articles/'
    index_filename = 'index.html'
    article_filename = 'article.html'
    site_directory = 'site/'
    templates_location = '/templates'

    article_template_location = '{}/{}'.format(templates_location, article_filename)
    index_template_location = '{}/{}'.format(templates_location, index_filename)
    index_result_location = '{}{}'.format(site_directory, index_filename)

    if not os.path.exists(site_directory): os.mkdir(site_directory)

    create_index(index_template_location, index_result_location, config)
    create_articles(article_template_location, articles_dir_location, site_directory, config)


if __name__ == '__main__':
    main()