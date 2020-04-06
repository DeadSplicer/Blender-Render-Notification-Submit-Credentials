# WHAT THIS DOES: Sends an email whenever your render is finished. It will not send you 1000 emails if you're rendering
#   a scene that is 1000 frames long.
#
# HOW TO USE:
# Replace the indicated info below to match your gmail, password, & sendto address (make sure you replace both sections)
#   (note: you can send messages from email accounts to your phone via SMS - ex. Verizon users can send to 1115551234@vtext.com to have it delivered as a text)
# Install as a Blender add-on: Edit > Preferences > Add-ons > Install...
# Then follow this link to allow less secure apps to use your gmail account (I recommend you make an account specifically for render notifications): https://myaccount.google.com/lesssecureapps
#
# My info if you care: This was originally created by Eric Charles (me), but since I don't know Python (I do more web design stuff), I hired GoofyGorilla on Reddit to basically rewrite it to work as an add-on.
# My art website is at ericcharl.es
# Venmo: @EricCharl-es (just in case, ya'know?)

bl_info = {
    "name" : "Render Notification - Hardcoded Credentials",
    "blender": (2, 81, 0),
    "category": "Render",
    "author": "Eric Charles, GoofyGorilla",
    "description": "Sends an email whenever your render is finished. Open .py file in text editor before installing as add-on."
}

import bpy
from bpy.app.handlers import persistent
from bpy.props import *

class  RenderNotif(bpy.types.Operator):
    """My Render Notification Addon"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "render.sendnotif"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Send notification after render is finished."         # Display name in the interface.

    @classmethod
    def render_notification(self):
        print("Render complete")

        import smtplib

#------------------------------- INSERT YOUR INFORMATION HERE -------------------------------------
        gmail_user = 'EXAMPLE@gmail.com'                     #Enter Gmail to send the message
        gmail_password = 'EX@MPLE-P@SSW0RD!'                       #Enter password for that Gmail account
        sent_from = 'EXAMPLE@gmail.com'                      #Enter Gmail to send the message (again)
        to = ['JON-SOMETHING@mailaddress.com']                           #Email to this address
#--------------------------------------------------------------------------------------------------


        subject = 'Blender has finished rendering!'
        filename = bpy.path.basename(bpy.context.blend_data.filepath)   #get the filename
        text = " has finished rendering."
        body = filename + text
        email_text = 'Subject: {}\n\n{}'.format(subject, body)


        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password) #  Exception here
        try:
            server.sendmail(gmail_user, to, email_text)
            print("Message sent successfully!")
        except:
            print("Failed to send message :(")
        server.quit()

    def execute(self, context):
        self.render_notification()
        return {'FINISHED'}



classes = (
    RenderNotif,
)

def menu_func(self, context):
    self.layout.operator(RenderNotif.bl_idname)

@persistent
def send_notification(dummy):
    print("Render complete")

    import smtplib

#------------------------------- INSERT YOUR INFORMATION HERE -------------------------------------
    gmail_user = 'EXAMPLE@gmail.com'                     #Enter Gmail to send the message
    gmail_password = 'EX@MPLE-P@SSW0RD!'                       #Enter password for that Gmail account
    sent_from = 'EXAMPLE@gmail.com'                      #Enter Gmail to send the message (again)
    to = ['JON-SOMETHING@mailaddress.com']                           #Email to this address
#--------------------------------------------------------------------------------------------------

    subject = 'Blender has finished rendering!'
    filename = bpy.path.basename(bpy.context.blend_data.filepath)   #get the filename
    text = " has finished rendering."
    body = filename + text
    email_text = 'Subject: {}\n\n{}'.format(subject, body)


    server = smtplib.SMTP('smtp.gmail.com:587')
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
