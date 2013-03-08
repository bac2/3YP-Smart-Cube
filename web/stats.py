from base_handler import BaseHandler
from data_objects import Cube, Profile, User, Transition, ProfileTransition
import tornado.web


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
