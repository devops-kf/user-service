from flask_restful import Resource


class UserProfilesResource(Resource):

    # GET /user-profiles/<profile_id>
    def get(self):
        pass

    # PUT /user-profiles/<profile_id>
    def put(self):
        pass


class FollowRelationshipsResource(Resource):

    # POST /user-profiles/<profile_id>/follow
    def post(self):
        pass

    # DELETE /user-profiles/<profile_id>/follow
    def delete(self):
        pass


class BlockRelationshipsResource(Resource):

    # POST /user-profiles/<profile_id>/block
    def post(self):
        pass

    # DELETE /user-profiles/<profile_id>/block
    def delete(self):
        pass


class MuteUserProfileResource(Resource):

    # PUT /user-profiles/<profile_id>/mute
    def put(self):
        pass


class UnMuteUserProfileResource(Resource):

    # /user-profiles/<profile_id>/un-mute
    def put(self):
        pass
