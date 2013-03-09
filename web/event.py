from base_handler import BaseHandler
from data_objects import User
import tornado.web

class EventHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        import json
        current_user = self.get_current_user()
        events = self.db.query("SELECT id AS event_id, action, rotation, (SELECT name FROM User WHERE id=(SELECT owner FROM Cube WHERE id=cube_id)) AS name, (SELECT (CASE rotation WHEN 1 THEN side1 WHEN 2 THEN side2 WHEN 3 THEN side3 WHEN 4 THEN side4 WHEN 5 THEN side5 WHEN 6 THEN side6 end) FROM Profile WHERE id=profile_id) AS side_name, cube_id FROM Event WHERE owner = %s AND action='sound' AND rotation = (SELECT position FROM Transition WHERE Transition.cube_id=Event.cube_id ORDER BY time DESC LIMIT 1) AND seen is NULL;", current_user.user_id)

        self.write(json.dumps(events))


class EventEditHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self, event_id):
        current_user = self.get_current_user()
        self.db.execute("UPDATE Event SET seen=NOW() WHERE id=%s AND owner=%s", event_id, current_user.user_id)

    @tornado.web.authenticated
    def delete(self, event_id):
        self.db.execute("DELETE FROM Event WHERE id=%s;", event_id);
        self.write("success")
            
