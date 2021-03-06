#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Nicolas Bétheuil 2019                                      ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from .Analyser_Merge import Analyser_Merge, Source, SHP, Load, Mapping, Select, Generate


class Analyser_merge_defibrillators_FR_hautevienne(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8370", "class": 60, "level": 3, "tag": ["merge"], "desc": T_(u"Defibrillator not integrated") }
        Analyser_Merge.__init__(self, config, logger,
            u"https://www.data.gouv.fr/fr/datasets/defibrillateur-automatise-externe-dae-haute-vienne/",
            u"défibrillateur automatisé externe DAE - Haute-Vienne",
            SHP(Source(attribution = u"GéoLimousin",
                    fileUrl = u"https://www.data.gouv.fr/fr/datasets/r/ff4418b6-87ac-489a-ba9d-7fdd03f4d116",
                    zip = u"dae_sdis87.shp")),
            Load(("ST_X(ST_Centroid(geom))",), ("ST_Y(ST_Centroid(geom))",), srid = 2154),
            Mapping(
                select = Select(
                    types = ["nodes", "ways", "relations"],
                    tags = {"emergency": "defibrillator"}),
                conflationDistance = 50,
                generate = Generate(
                    static1 = {"emergency": "defibrillator"},
                    static2 = {"source": self.source} )))
