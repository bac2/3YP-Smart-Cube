from base_handler import BaseHandler
from data_objects import Cube, Profile, User, Transition
import datetime
import json
import tornado.web

class TransitionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, Transition):
            return { 'time':obj.time, 'position':obj.position, 'side_name':obj.side_name}

class StatsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
            self.params['cubes'] = self.get_cubes()

            self.render("stats.html", **self.params)

class StatsDataHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, cube_id):
        self.write(self.get_transitions(cube_id))

    def get_transitions(self, cube_id):
        transitions = self.db.query("SELECT position, time, cube_id, (SELECT (case position when 1 then side1 WHEN 2 THEN side2 WHEN 3 THEN side3 WHEN 4 THEN side4 WHEN 5 THEN side5 WHEN 6 THEN side6 end) AS side_name FROM ProfileTransition INNER JOIN Profile ON Profile.id = ProfileTransition.profile_id WHERE ProfileTransition.cube_id=%s ORDER BY ProfileTransition.time DESC LIMIT 1) AS sidename FROM Transition WHERE cube_id=%s AND time > (SELECT time FROM ProfileTransition WHERE cube_id=%s ORDER BY time DESC LIMIT 1);", cube_id, cube_id, cube_id)

        transition_list = []
        for transition_info in transitions:
            transition_list.append( Transition(transition_info) )	
        return json.dumps(transition_list, cls=TransitionEncoder)
