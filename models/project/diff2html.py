# -*- coding: utf-8 -*-

from odoo import models, fields, api
import os
import codecs

DIRECTORY = '/opt/nagini'
TMP = '/home/ramesh/Downloads/mohini'
PROJECT = 'Nagini'


class Diff2HTML(models.TransientModel):
    _name = "diff.html"

    name = fields.Char(string="Name", default=PROJECT)
    diectory_path = fields.Char(string="Directory Path", default=DIRECTORY)
    commit_ids = fields.One2many(comodel_name="git.commit", inverse_name="diff_id")

    @api.multi
    def trigger_get_commits(self):
        detail = []
        location = "{0}/diff_{1}.txt".format(TMP, self.id)
        command = "cd {0} && git log --pretty=oneline > {1}".format(DIRECTORY, location)
        os.system(command)

        with open(location) as commits:
            for commit in commits:
                data = commit.split(" ", 1)
                if len(data) == 2:
                    detail.append((0, 0, {"name": data[1], "reference": data[0]}))

        self.commit_ids = detail


class GitCommit(models.TransientModel):
    _name = "git.commit"

    name = fields.Char(string="Name")
    reference = fields.Char(string="Reference")
    diff_html = fields.Html(string="Diff HTML", compute="_get_diff_html")
    diff_id = fields.Many2one(comodel_name="diff.html", string="Diff HTML")

    def _get_diff_html(self):
        if self.reference:
            location = "{0}/commit_{1}.html".format(TMP, self.id)
            command = "cd {0} && diff2html -s side -f html -o stdout -- {1} > {2}".format(DIRECTORY, self.reference, location)
            os.system(command)
            data = codecs.open(location, 'r')
            html = data.read()
            html = html.replace('<h1>Diff to HTML by <a href="https://github.com/rtfpessoa">rtfpessoa</a></h1>', '')
            self.diff_html = html








