import os
import sys
from timeit import default_timer as timer
from datetime import datetime, timedelta
import logging

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

log = logging.getLogger('mkdocs')

class ConfidentialPlugin(BasePlugin):

    config_scheme = (
        ('default_classification', config_options.Type(str, default='unclassified')),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    # def on_serve(self, server):
    #     return server

    # def on_pre_build(self, config):
        # return

    def on_files(self, files, config):
        for f in files:
            f.dest_path = f.dest_path.replace(' ', '_')
            f.abs_dest_path = f.abs_dest_path.replace(' ', '_')
            f.url = f._get_url(config['use_directory_urls'])
        return files

    # def on_nav(self, nav, config, files):
        # return nav

    # def on_env(self, env, config, site_nav):
        # return env
    
    # def on_config(self, config):
        # return config

    # def on_post_build(self, config):
        # return

    # def on_pre_template(self, template, template_name, config):
        # return template

    # def on_template_context(self, context, template_name, config):
    #     return context
    
    # def on_post_template(self, output_content, template_name, config):
    #     return output_content
    
    # def on_pre_page(self, page, config, files):
    #     return page

    def on_page_read_source(self, page, config):
        with open(page.file.abs_src_path) as f:
            contents = f.read()
            if contents[:3] != "---":
                contents = "---\nclassified: {}\n---\n\n".format(self.config['default_classification']) + contents
        return contents

    def on_page_markdown(self, markdown, page, config, files):
        log.info(page.file.dest_path)
        log.info(page.meta)
        return markdown

    # def on_page_content(self, html, page, config, files):
    #     return html

    # def on_page_context(self, context, page, config, nav):
    #     return context

    def on_post_page(self, output_content, page, config):
        if "classified" in page.meta and page.meta["classified"].lower() != "unclassified":
            # log.warn("Skipping classified page %s", page.title)
            return ""
        return output_content

