from base_handler import BaseHandler
from data_objects import Cube, Profile, User, Transition, ProfileTransition
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
            for cube in self.params['cubes']:
                cube.profile_transitions = self.get_profile_transitions(cube)

            self.render("stats.html", **self.params)

    def get_profile_transitions(self, cube):
        ptrans = self.db.query("SELECT ProfileTransition.time AS time, cube_id, ProfileTransition.id AS id, Profile.name as name FROM ProfileTransition INNER JOIN Profile ON Profile.id = ProfileTransition.profile_id WHERE cube_id=%s ORDER BY ProfileTransition.time DESC;", cube.cube_id)

        ptransitions = []
        for ptran in ptrans:
           ptransitions.append(ProfileTransition(ptran))
        return ptransitions


class StatsDataHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, cube_id, profile_transition_id):
        self.write(self.get_transitions(cube_id, profile_transition_id))
    def get_transitions(self, cube_id, profile_transition_id):
        transitions = self.db.query("SELECT position, time, cube_id, (SELECT (case position when 1 then side1 WHEN 2 THEN side2 WHEN 3 THEN side3 WHEN 4 THEN side4 WHEN 5 THEN side5 WHEN 6 THEN side6 end) AS side_name FROM ProfileTransition INNER JOIN Profile ON Profile.id = ProfileTransition.profile_id WHERE ProfileTransition.id=%s ORDER BY ProfileTransition.time DESC LIMIT 1) AS sidename FROM Transition WHERE cube_id=%s AND time BETWEEN (SELECT time FROM ProfileTransition WHERE id=%s AND ProfileTransition.cube_id=Transition.cube_id) AND (SELECT time FROM ProfileTransition WHERE id=%s AND ProfileTransition.cube_id=Transition.cube_id UNION (SELECT NOW() FROM DUAL) ORDER BY time ASC LIMIT 1);", str(profile_transition_id), str(cube_id), str(profile_transition_id), str(int(profile_transition_id)+1))

        transition_list = []
        for transition_info in transitions:
            transition_list.append( Transition(transition_info) )	
        return json.dumps(transition_list, cls=TransitionEncoder)
