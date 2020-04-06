# WHAT THIS DOES: Sends an email whenever your render is finished. It will not send you 1000 emails if you're rendering
#   a scene that is 1000 frames long.
#
# HOW TO USE: Install as a Blender add-on: Edit > Preferences > Add-ons > Install...
# In 3D view, select the Object dropdown menu, then "Set emails and password"
# Then enter the email that you want to send the message from (must be a gmail account), the password for that email, and the email address that you want the message to be sent to
#   (note: you can send messages from email accounts to your phone via SMS - ex. Verizon users can send to 1115551234@vtext.com to have it delivered as a text)
# Then follow this link to allow less secure apps to use your gmail account (I recommend you make an account specifically for render notifications): https://myaccount.google.com/lesssecureapps
#
# My info if you care: This was originally created by Eric Charles, but since I don't know Python (I do more web design stuff), I hired GoofyGorilla on Reddit to basically rewrite it to work as an add-on.
# My art website is at ericcharl.es
# Venmo: @EricCharl-es (just in case, ya'know?)

bl_info = {
    "name" : "Render Notification - Submit Credentials",
    "blender": (2, 81, 0),
    "category": "Render",
    "author": "Eric Charles, GoofyGorilla",
    "description": "Sends an email whenever your render is finished. Go to 3D_View > Object > Set emails and password to enable"
}

import bpy
from bpy.app.handlers import persistent
from bpy.props import *
from bpy.types import Operator, AddonPreferences
import requests
import json
import re

class  RenderNotifParams(bpy.types.Operator):
    """Set the email username and password"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "wm.rendernotifparams"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Set emails and password"         # Display name in the interface.

    email : bpy.props.StringProperty(name= "Enter Email (from)", default= "")
    password : bpy.props.StringProperty(name= "Enter Password (from)", default= "")
    toEmail : bpy.props.StringProperty(name= "Enter Email (to)", default= "")

    def execute(self, context):
        bpy.types.Scene.email = self.email
        bpy.types.Scene.password = self.password
        bpy.types.Scene.toEmail = self.toEmail

        message = "%s, %s, %s" % (self.email,
            self.password, self.toEmail)
        self.report({'INFO'}, message)
        print(message)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

classes = (
    RenderNotifParams,
)

def menu_func(self, context):
    self.layout.operator(RenderNotifParams.bl_idname)

@persistent
def send_notification(dummy):
    print("Render complete")

    import smtplib

    gmail_user = bpy.context.scene.email                  #Enter Gmail to send the message
    gmail_password = bpy.context.scene.password                      #Enter password for that Gmail account
    sent_from = bpy.context.scene.email                      #Enter Gmail to send the message (again)
    to = [bpy.context.scene.toEmail]                           #Email to this (Verizon) number


    subject = 'Blender has finished rendering!'
    filename = bpy.path.basename(bpy.context.blend_data.filepath)   #get the filename
    text = " has finished rendering."
    body = filename + text
    email_text = 'Subject: {}\n\n{}'.format(subject, body)
    print(gmail_user)
    response = requests.get("https://emailsettings.firetrust.com/settings?q=" + gmail_user)
    resp_parsed = re.sub(r'^jsonp\d+\(|\)\s+$', '', response.text)
    data = json.loads(resp_parsed)
    responseAddress = data['settings'][2]['address']

    server = smtplib.SMTP(responseAddress + ':587')
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password) #  Exception here
    try:
        server.sendmail(gmail_user, to, email_text)
        print("Message sent successfully!")
    except:
        print("Failed to send message :(")
    server.quit()

def register():
    bpy.app.handlers.render_complete.append(send_notification)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    bpy.app.handlers.render_complete.remove(send_notification)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()
