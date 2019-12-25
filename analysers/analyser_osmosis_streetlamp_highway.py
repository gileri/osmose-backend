#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015                                      ##
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

from .Analyser_Osmosis import Analyser_Osmosis

sql10 = """
CREATE TEMPORARY TABLE lit_highways AS
SELECT ST_Buffer(w.linestring::geography, 15) as linestring
FROM highways w
WHERE w.tags ? 'highway'
AND w.tags->'lit' = 'yes';
"""

sql11= """
SELECT
  n.id,
  ST_AsText(n.geom)
FROM nodes AS n
WHERE n.tags->'highway' = 'street_lamp'
AND NOT EXISTS (
  SELECT w.linestring
  FROM lit_highways AS w
  WHERE ST_Intersects(n.geom::geography, w.linestring::geography));
"""

class Analyser_Osmosis_Streetlamp_Highway(Analyser_Osmosis):

    requires_tables_common = ['highways']

    def __init__(self, config, logger=None):
        Analyser_Osmosis.__init__(self, config, logger)
        self.classs[1] = {"item": "1234", "level": 1, "tag": ["highway", "fix:chair"], "desc": T_(u"Street lamp without a lit highway")}

    def analyser_osmosis_common(self):
        self.run(sql10)
        self.run(sql11, lambda res: {
            "class": 1,
            "data": [self.node_full, self.positionAsText]})
