from flask_mail import Message
from bson.objectid import ObjectId

def send_confirmation(attorney_id, email_address):
	subject="Edit Your CapitalProBono.org entry"
	body="<p>Thank you for registering for capitalprobono.org. To edit your entry, please click the following address: <a href='https://capitalprobono.org/attorneys/" + str(ObjectId(attorney_id)) + "'>https://capitalprobono.org/attorneys/" + str(ObjectId(attorney_id)) + "</a>.</p><pIf you have any difficulty, please contact capitalprobono@esq.io.</p><p>Thank you!</p>"
	sender="do-not-reply@capitalprobono.org"
	from_name='Capital Pro Bono Honor Roll'
	return {"from_email":sender, "from_name":from_name, "subject":subject, "html":body, "to":[{'email': email_address}]}