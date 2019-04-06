import os

from uuid import uuid4

from flask import request
from flask_restful import Resource,reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, get_jwt_claims

from server.flaskr import app
from server.flaskr.models import modelHelpers
from server.flaskr.API import apiServer

parser = reqparse.RequestParser()
parser.add_argument("acctType")
parser.add_argument("ID")
parser.add_argument("name")
parser.add_argument("detailType")
parser.add_argument("detailValue")
parser.add_argument("username")
parser.add_argument("password")
parser.add_argument("code")
parser.add_argument("progLang")
parser.add_argument("questions")

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if(data["acctType"]=="Student"):
            if(modelHelpers.isExistingStudentByID(data["ID"])):
                return {"message":"User already exists, please login in login page"}

            else:
                # try:
                modelHelpers.insertIntoStudent(
                    ID=data["ID"],
                    name=data["name"],
                    semester=data["detailValue"],
                    username = data["username"],
                    password = data["password"]
                )
                print("here")
                accessToken = create_access_token(identity = data["username"])
                refreshToken = create_refresh_token(identity = data["username"])
                return {
                    "success": "Student {} was created".format(data["username"]),
                    "accessToken": accessToken,
                    "refreshToken": refreshToken
                }
                
                # except:
                #     return {"error": "Something went wrong"}, 500

        else:
            if(modelHelpers.isExistingTeacherByID(data["ID"])):
                return {"message":"User already exists, please login in login page"}

            else:
                try:
                    modelHelpers.insertIntoTeacher(
                        ID=data["ID"],
                        name=data["name"],
                        designation=data["detailValue"],
                        username = data["username"],
                        password = data["password"]
                    )
                    accessToken = create_access_token(identity = data["username"])
                    refreshToken = create_refresh_token(identity = data["username"])
                    return {
                        "success": "Teacher {} was created".format(data["username"]),
                        "accessToken": accessToken,
                        "refreshToken": refreshToken
                    }
                    
                except:
                    return {"error": "Something went wrong"}, 500


class UserLogin(Resource):
    def post(self):        
        data = parser.parse_args()

        if(data["acctType"]=="Student"):
            currentUser = modelHelpers.isExistingStudentByUsername(data["username"])
        else:
            currentUser = modelHelpers.isExistingTeacherByUsername(data["username"])

        if not currentUser:
            return {"error": "User {} doesn't exist".format(data["username"])}
        
        if(data["acctType"]=="Student"):
            currentUser = modelHelpers.getStudentByUsername(data["username"])
        else:
            currentUser = modelHelpers.getTeacherByUsername(data["username"])

        if data["password"] == currentUser.password:
            accessToken = create_access_token(identity = data["username"])
            refreshToken = create_refresh_token(identity = data["username"])

            return {
                "success": "Logged in as {}".format(currentUser.username),
                "accessToken": accessToken,
                "refreshToken": refreshToken
            }

        else:
            return {"error": "Wrong credentials"},500

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        JTI = get_raw_jwt()["jti"]
        try:
            revokedToken = modelHelpers.insertIntoRevokedTokens(JTI = JTI)
            return {"message": "Access token has been revoked"}
        except:
            return {"message": "Something went wrong"}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        JTI = get_raw_jwt()["jti"]
        try:
            revokedToken = modelHelpers.insertIntoRevokedTokens(JTI = JTI)
            return {"message": "Refresh token has been revoked"}
        except:
            return {"message": "Something went wrong"}, 500

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        currentUser = get_jwt_identity()
        accessToken = create_access_token(identity = currentUser)
        return {"access_token": accessToken}

class GetStudentDetails(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        username = claims["username"]
        res = modelHelpers.getStudentByUsername(username)

        return {
            "ID":res.ID,
            "name":res.name,
            "username":res.username,
            "semester":res.semester,
            "noOfChallenges":res.noOfChallenges
        }

class GetTeacherDetails(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        username = claims["username"]
        res = modelHelpers.getTeacherByUsername(username)

        return {
            "ID":res.ID,
            "name":res.name,
            "username":res.username,
            "designation":res.designation,
            "noOfChallenges":res.noOfChallenges
        }


# This class will represent all hidden routes
class UploadCode(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        username = claims["username"]

        # Get Student details by username
        # Then convert into a JSON

        # Read incoming JSON
        # JSON Structure as Key-Value pairs (proposed):
        # +--------------+---------+
        # | USN          | String  |
        # | code         | String  |
        # | progLang     | String  |
        # | questionHash | String  |
        # +--------------+---------+
        #
        inputJson = dict(request.form)
        inputJson.update({key:value[0] for key, value in inputJson.items()})
        inputJson['code'] = request.files['code'].stream.read().decode()
        print(inputJson)

        # Get output Dictionary
        output = apiServer.uploadCode(inputJson)


        # JSON Structure as Key-Value pairs (proposed):
        # +--------+--------+
        # | input  | JSON   |
        # | output | String |
        # +--------+--------+
        #

        outputJson = jsonify({
                "input":inputJson,
                "output":output
        })

        return outputJson, 201


class SetChallenge(Resource):
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        username = claims["username"]

        teacherID = modelHelpers.getTeacherByUsername(username).ID

        questions = request.get_json()["questions"]
        timeLimitHrs = request.get_json()["timeLimitHrs"]
        timeLimitMins = request.get_json()["timeLimitMins"]

        TEST_CASES_FOLDER = app.config["TEST_CASES_FOLDER"]
        EXPECTED_OUTPUTS_FOLDER = app.config["EXPECTED_OUTPUTS_FOLDER"]

        # Create a UUID $uuid1
        # Create a models.Challenge entry with UUID $uuid1, teacherID, status="INACTIVE", timeLimitHrs, timeLimitMins

        challengeID = uuid4().time #18 character long unique ID
        modelHelpers.insertIntoChallenge(
            ID=challengeID,
            teacherID=teacherID,
            status="INACTIVE",
            timeLimitHrs=timeLimitHrs,
            timeLimitMins=timeLimitMins
        )

        # For each question in questions:
        #   Create a UUID $uuid2
        #   Create a models.Question entry with UUID $uuid2, name=question.questionName, CPU=question.cpu, memory=question.memory 
        #   For each testCase,expectedOutput in question.testCase,question.expectedOutput:
        #       Create a UUID #uuid3
        #       Make a file each for testCase and expectedOutput
        #       Create a models.TestCase entry with: $uuid3, testCase filePath, expectedOutput filePath
        #       Create a models.QuestionAndTestCase entry with $uuid2,$uuid3
        #   
        #   Create a models.ChallengeAndQuestion entry with $uuid1,$uuid2


        for question in questions:
            questionID = uuid4().time
            modelHelpers.insertIntoQuestion(
                ID=questionID,
                name=question["questionName"],
                CPU=question["cpu"],
                memory=question["memory"]
            )

            for testCase,expectedOutput in zip(question["testCases"],question["expectedOutputs"]):
                testCaseID = uuid4().time
                testCasePath = os.path.join(TEST_CASES_FOLDER,str(testCaseID))
                expectedOutputPath = os.path.join(EXPECTED_OUTPUTS_FOLDER,str(testCaseID))

                with open(testCasePath,"w") as fp:
                    fp.write(testCase)

                with open(expectedOutputPath,"w") as fp:
                    fp.write(expectedOutput)

                modelHelpers.insertIntoTestCase(
                    ID=testCaseID,
                    testCasePath=testCasePath,
                    expectedOutputPath=expectedOutputPath
                )

                modelHelpers.insertIntoQuestionAndTestCase(
                    qID=questionID,
                    tID=testCaseID
                )

            modelHelpers.insertIntoChallengeAndQuestion(
                cID=challengeID,
                qID=questionID
            )