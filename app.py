from flask import Config, Flask, jsonify,request
from decouple import config
import firebase_admin
import requests
from flask_cors import CORS
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from firebase_admin import auth ,exceptions
import cloudinary
import cloudinary.uploader
import cloudinary
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializar Cloudinary
cloudinary.config( 
  cloud_name = config("CLOUD_NAME"), 
  api_key = config("API_KEY"), 
  api_secret = config("API_SECRET_KEY"),
  secure = True
)
# Inicializar JSONBin
key_json=config('KEY')
url = config('URL_CREDENTIALS_FIREBASE')
headers = {
  'X-Master-Key': key_json
}
req = requests.get(url, json=None, headers=headers)
data=req.json()["record"]

# Credenciales Firebase
cred = credentials.Certificate(data)
url=config('URL_FIREBASE')

#Inicializar Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': url,
})

# API Email SendGrid

def sendEmail(email,name,case):
  
  if case==1:
    subject=f'Bienvenido a Nuovent {name} '
    content='''<td>
                            <!--[if mso]>
    <center>
    <table><tr><td width="600">
  <![endif]-->
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:600px;" align="center">
                                      <tbody><tr>
                                        <td role="modules-container" style="padding:0px 0px 0px 0px; color:#516775; text-align:left;" bgcolor="#F9F5F2" width="100%" align="left"><table class="module preheader preheader-hide" role="module" data-type="preheader" border="0" cellpadding="0" cellspacing="0" width="100%" style="display: none !important; mso-hide: all; visibility: hidden; opacity: 0; color: transparent; height: 0; width: 0;">
    <tbody><tr>
      <td role="module-content">
        <p>Bienvenido a Nuovent</p>
      </td>
    </tr>
  </tbody></table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="bdzDb4B4pnnez4W7L1KpxJ">
      <tbody><tr>
        <td style="padding:0px 0px 30px 0px;" role="module-content" bgcolor="">
        </td>
      </tr>
    </tbody></table><table class="wrapper" role="module" data-type="image" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="572c1c6a-0a31-4dec-aefd-075ab9e5cda4">
    <tbody>
      <tr>
        <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center">
          <img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:100% !important; width:100%; height:auto !important;" width="600" alt="" data-proportionally-constrained="true" data-responsive="true" src="http://cdn.mcauto-images-production.sendgrid.net/6c29d3a10ca3a34b/b1de1558-0d65-4e0c-b291-75121c6138bf/1004x590.png">
        </td>
      </tr>
    </tbody>
  </table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="gNWHzBzkFeWH4JDKd2Aikk" data-mc-module-version="2019-10-22">
      <tbody><tr>
        <td style="background-color:#F9F5F2; padding:50px 0px 10px 0px; line-height:30px; text-align:inherit;" height="100%" valign="top" bgcolor="#F9F5F2"><div><div style="font-family: inherit; text-align: center"><span style="color: #516775; font-size: 28px; font-family: georgia, serif"><strong>Bienvenido a Nuovent!</strong></span></div><div></div></div></td>
      </tr>
    </tbody></table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="bA2FfEE6abadx6yKoMr3F9" data-mc-module-version="2019-10-22">
      <tbody><tr>
        <td style="padding:10px 40px 50px 40px; line-height:22px; text-align:inherit; background-color:#F9F5F2;" height="100%" valign="top" bgcolor="#F9F5F2"><div><h1 style="text-align: center">Encuentra tu espacio ideal</h1>
<div style="font-family: inherit; text-align: center"><span style="box-sizing: border-box; margin-top: 0px; margin-bottom: 1rem; font-size: 1.25rem; font-weight: 300; font-family: -apple-system, BlinkMacSystemFont, &quot;Segoe UI&quot;, Roboto, Oxygen, Ubuntu, Cantarell, &quot;Fira Sans&quot;, &quot;Droid Sans&quot;, &quot;Helvetica Neue&quot;, sans-serif; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; letter-spacing: normal; orphans: 2; text-align: center; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(248, 249, 250); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; color: #101010">Mira espacios para realizar tu evento ideal en el lugar perfecto para ti y tu invitados; haz que los momentos más importantes en la vida, tengan una celebración especial, Nuovent.com te ayuda a encontrar y contactar directamente con los prestadores de los servicios y espacios para la realización de eventos.</span><span style="color: #101010">&nbsp;</span></div><div></div></div></td>
      </tr>
    </tbody></table><table border="0" cellpadding="0" cellspacing="0" class="module" data-role="module-button" data-type="button" role="module" style="table-layout:fixed;" width="100%" data-muid="39993cb2-a42d-4dff-9244-d7e64c4cf5e2">
      <tbody>
        <tr>
          <td align="center" bgcolor="" class="outer-td" style="padding:0px 0px 0px 0px;">
            <table border="0" cellpadding="0" cellspacing="0" class="wrapper-mobile" style="text-align:center;">
              <tbody>
                <tr>
                <td align="center" bgcolor="#20A2E8" class="inner-td" style="border-radius:6px; font-size:16px; text-align:center; background-color:inherit;">
                  <a href="" style="background-color:#20A2E8; border:1px solid #333333; border-color:#333333; border-radius:6px; border-width:1px; color:#ffffff; display:inline-block; font-size:14px; font-weight:normal; letter-spacing:0px; line-height:normal; padding:12px 18px 12px 18px; text-align:center; text-decoration:none; border-style:solid;" target="_blank">Ver Anuncios</a>
                </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table><table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="qkG1GEG4EZSwoAzbwgoD8v">
      <tbody><tr>
        <td style="padding:0px 0px 0px 0px;" role="module-content" height="100%" valign="top" bgcolor="">
          <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="10px" style="line-height:10px; font-size:10px;">
            <tbody><tr>
              <td style="padding:0px 0px 10px 0px;" bgcolor=""></td>
            </tr>
          </tbody></table>
        </td>
      </tr>
    </tbody></table><table class="module" role="module" data-type="social" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="811a4d90-5cf8-4edd-afaf-8d7ae129dd7e">
    <tbody>
      <tr>
        <td valign="top" style="padding:0px 0px 0px 0px; font-size:6px; line-height:10px;" align="center">
          <table align="center" style="-webkit-margin-start:auto;-webkit-margin-end:auto;">
            <tbody><tr align="center"><td style="padding: 0px 5px;" class="social-icon-column">
      <a role="social-icon-link" href="https://facebook.com" target="_blank" alt="Facebook" title="Facebook" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
        <img role="social-icon" alt="Facebook" title="Facebook" src="https://mc.sendgrid.com/assets/social/white/facebook.png" style="height:30px; width:30px;" height="30" width="30">
      </a>
    </td><td style="padding: 0px 5px;" class="social-icon-column">
      <a role="social-icon-link" href="https://twitter.com" target="_blank" alt="Twitter" title="Twitter" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
        <img role="social-icon" alt="Twitter" title="Twitter" src="https://mc.sendgrid.com/assets/social/white/twitter.png" style="height:30px; width:30px;" height="30" width="30">
      </a>
    </td><td style="padding: 0px 5px;" class="social-icon-column">
      <a role="social-icon-link" href="https://instagram.com" target="_blank" alt="Instagram" title="Instagram" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
        <img role="social-icon" alt="Instagram" title="Instagram" src="https://mc.sendgrid.com/assets/social/white/instagram.png" style="height:30px; width:30px;" height="30" width="30">
      </a>
    </td><td style="padding: 0px 5px;" class="social-icon-column">
      <a role="social-icon-link" href="https://www.pinterest.com/sendgrid/" target="_blank" alt="Pinterest" title="Pinterest" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
        <img role="social-icon" alt="Pinterest" title="Pinterest" src="https://mc.sendgrid.com/assets/social/white/pinterest.png" style="height:30px; width:30px;" height="30" width="30">
      </a>
    </td></tr></tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="f5F8P1n4pQyU8o7DNMMEyW">
      <tbody><tr>
        <td style="padding:0px 0px 30px 0px;" role="module-content" bgcolor="">
        </td>
      </tr>
    </tbody></table></td>
                                      </tr>
                                    </tbody></table>
                                    <!--[if mso]>
                                  </td>
                                </tr>
                              </table>
                            </center>
                            <![endif]-->
                          </td>'''
  else:
   subject=f'Nuevo anuncio creado'
   content=""" <div class="Content_PI7HK" id="design-editor-email-body-wrap" style="background-color: rgb(249, 245, 242); color: rgb(81, 103, 117); font-size: 16px; font-family: verdana, geneva, sans-serif;"><style>
          #design-editor-email-body-wrap a {
            color: #993300
          }
        </style><div class="email-body_2DUY1" id="editor-email-body" style="width: 600px; background-color: rgb(249, 245, 242); padding: 0px;"><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="text-module" data-muid="a1e5c40a-ec5a-4714-a92c-6986c7890e13"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">text</h4><div class="module-controls-right_1wNFJ"><div data-role="code" class="module-control module-control_3tr60"><span data-tooltip="Edit Module HTML" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-code sg-icon_3W7YJ sg-icon-code_3raq-" tabindex="-1" data-role="edit-module-html"></i></span></span></div><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="a1e5c40a-ec5a-4714-a92c-6986c7890e13" data-mc-module-version="2019-10-22">
    <tbody>
      <tr>
        <td style="padding:18px 0px 18px 0px; line-height:22px; text-align:inherit;" height="100%" valign="top" bgcolor="" role="module-content"><div><div style="font-family: inherit; text-align: right"><span style="box-sizing: border-box; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-numeric: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-size: 10px; vertical-align: baseline; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px; border-top-style: initial; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image-source: initial; border-image-slice: initial; border-image-width: initial; border-image-outset: initial; border-image-repeat: initial; color: #000000; letter-spacing: normal; orphans: 2; text-align: right; text-indent: 0px; text-transform: none; white-space: pre-wrap; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(247, 247, 247); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; font-family: arial, helvetica, sans-serif">Email not displaying correctly? </span><a href="{{Weblink}}"><span style="box-sizing: border-box; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-numeric: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-size: 10px; vertical-align: baseline; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px; border-top-style: initial; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image-source: initial; border-image-slice: initial; border-image-width: initial; border-image-outset: initial; border-image-repeat: initial; outline-color: initial; outline-style: none; outline-width: initial; color: #0055b8; text-decoration-line: none; text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; transition-duration: 0.3s; transition-timing-function: ease; transition-delay: 0s; transition-property: color; letter-spacing: normal; orphans: 2; text-align: right; text-indent: 0px; text-transform: none; white-space: pre-wrap; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(247, 247, 247); font-family: arial, helvetica, sans-serif">View it</span></a><span style="box-sizing: border-box; padding-top: 0px; padding-right: 0px; padding-bottom: 0px; padding-left: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; margin-left: 0px; font-style: inherit; font-variant-ligatures: inherit; font-variant-caps: inherit; font-variant-numeric: inherit; font-variant-east-asian: inherit; font-weight: inherit; font-stretch: inherit; line-height: inherit; font-size: 10px; vertical-align: baseline; border-top-width: 0px; border-right-width: 0px; border-bottom-width: 0px; border-left-width: 0px; border-top-style: initial; border-right-style: initial; border-bottom-style: initial; border-left-style: initial; border-top-color: initial; border-right-color: initial; border-bottom-color: initial; border-left-color: initial; border-image-source: initial; border-image-slice: initial; border-image-width: initial; border-image-outset: initial; border-image-repeat: initial; color: #000000; letter-spacing: normal; orphans: 2; text-align: right; text-indent: 0px; text-transform: none; white-space: pre-wrap; widows: 2; word-spacing: 0px; -webkit-text-stroke-width: 0px; background-color: rgb(247, 247, 247); text-decoration-thickness: initial; text-decoration-style: initial; text-decoration-color: initial; font-family: arial, helvetica, sans-serif"> in your browser.</span></div><div></div></div></td>
      </tr>
    </tbody>
  </table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="image-module" data-muid="qa8oMphYHuL7xyQrTVscgD"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">image</h4><div class="module-controls-right_1wNFJ"><div data-role="code" class="module-control module-control_3tr60"><span data-tooltip="Edit Module HTML" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-code sg-icon_3W7YJ sg-icon-code_3raq-" tabindex="-1" data-role="edit-module-html"></i></span></span></div><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb has-overlay"><div class="reset"><table class="wrapper" role="module" data-type="image" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="qa8oMphYHuL7xyQrTVscgD">
      <tbody><tr>
        <td style="font-size:6px; line-height:10px; padding:30px 0px 0px 0px;" valign="top" align="center"><img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:100% !important; width:100%; height:auto !important;" src="http://cdn.mcauto-images-production.sendgrid.net/6c29d3a10ca3a34b/b1de1558-0d65-4e0c-b291-75121c6138bf/1004x590.png" alt="Ingrid &amp; Anders" width="600" data-responsive="true" data-proportionally-constrained="false"></td>
      </tr>
    </tbody></table></div><div class="module-overlay_1sK_n module-overlay-edit_3wJhn"><div class="module-overlay-content_37Fnu"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-image sg-icon_3W7YJ sg-icon-image_1A4LX" tabindex="-1"></i></span><span class="small">edit image</span></div></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="spacer-module" data-muid="bdzDb4B4pnnez4W7L1KpxJ"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">spacer</h4><div class="module-controls-right_1wNFJ"><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="bdzDb4B4pnnez4W7L1KpxJ">
      <tbody><tr>
        <td style="padding:0px 0px 30px 0px;" role="module-content" bgcolor="">
        </td>
      </tr>
    </tbody></table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="text-module" data-muid="gNWHzBzkFeWH4JDKd2Aikk"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">text</h4><div class="module-controls-right_1wNFJ"><div data-role="code" class="module-control module-control_3tr60"><span data-tooltip="Edit Module HTML" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-code sg-icon_3W7YJ sg-icon-code_3raq-" tabindex="-1" data-role="edit-module-html"></i></span></span></div><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="gNWHzBzkFeWH4JDKd2Aikk" data-mc-module-version="2019-10-22">
      <tbody><tr>
        <td style="background-color:#ffffff; padding:50px 0px 10px 0px; line-height:30px; text-align:inherit;" height="100%" valign="top" bgcolor="#ffffff"><div><div style="font-family: inherit; text-align: center"><span style="color: #516775; font-size: 28px; font-family: georgia, serif"><strong>Felicidades creaste un nuevo anuncio&nbsp;</strong></span></div><div></div></div></td>
      </tr>
    </tbody></table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="text-module" data-muid="bA2FfEE6abadx6yKoMr3F9"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">text</h4><div class="module-controls-right_1wNFJ"><div data-role="code" class="module-control module-control_3tr60"><span data-tooltip="Edit Module HTML" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-code sg-icon_3W7YJ sg-icon-code_3raq-" tabindex="-1" data-role="edit-module-html"></i></span></span></div><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="bA2FfEE6abadx6yKoMr3F9" data-mc-module-version="2019-10-22">
      <tbody><tr>
        <td style="background-color:#ffffff; padding:10px 40px 50px 40px; line-height:22px; text-align:inherit;" height="100%" valign="top" bgcolor="#ffffff"><div><div style="font-family: inherit; text-align: center"><span style="font-family: verdana, geneva, sans-serif">Ahora tus espacios estarán visibles para &nbsp;realizar un evento en &nbsp;Nuovent.com.</span></div><div></div></div></td>
      </tr>
    </tbody></table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="button-module" data-muid="bKHWQMgPkL5opYCkxiM6aS"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">button</h4><div class="module-controls-right_1wNFJ"><div data-role="code" class="module-control module-control_3tr60"><span data-tooltip="Edit Module HTML" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-code sg-icon_3W7YJ sg-icon-code_3raq-" tabindex="-1" data-role="edit-module-html"></i></span></span></div><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table border="0" cellpadding="0" cellspacing="0" class="module" data-role="module-button" data-type="button" role="module" style="table-layout:fixed" width="100%" data-muid="bKHWQMgPkL5opYCkxiM6aS"><tbody><tr><td align="center" class="outer-td" style="padding:20px 0px 0px 0px;" bgcolor=""><table border="0" cellpadding="0" cellspacing="0" class="button-css__deep-table___2OZyb wrapper-mobile" style="text-align:center"><tbody><tr><td align="center" bgcolor="#489BE8" class="inner-td" style="border-radius:6px; font-size:16px; text-align:center; background-color:inherit;"><a style="border:1px solid #993300; border-color:#993300; border-radius:0px; border-width:1px; color:#ffffff; display:inline-block; font-family:verdana,geneva,sans-serif; font-size:16px; font-weight:normal; letter-spacing:1px; line-height:30px; padding:12px 20px 12px 20px; text-align:center; text-decoration:none; border-style:solid; background-color:#489BE8;" href="https://nuovent.pages.dev/Zonaeventos" target="_blank">Ver Anuncios</a></td></tr></tbody></table></td></tr></tbody></table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="spacer-module" data-muid="qkfYAswHNSwNpwb1p7m4gC"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">spacer</h4><div class="module-controls-right_1wNFJ"><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="qkfYAswHNSwNpwb1p7m4gC">
      <tbody><tr>
        <td style="padding:0px 0px 30px 0px;" role="module-content" bgcolor="">
        </td>
      </tr>
    </tbody></table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="divider-module" data-muid="qkG1GEG4EZSwoAzbwgoD8v"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">divider</h4><div class="module-controls-right_1wNFJ"><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="qkG1GEG4EZSwoAzbwgoD8v">
      <tbody><tr>
        <td style="padding:0px 0px 0px 0px;" role="module-content" height="100%" valign="top" bgcolor="">
          <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="10px" style="line-height:10px; font-size:10px;">
            <tbody><tr>
              <td style="padding:0px 0px 10px 0px;" bgcolor="#ffffff"></td>
            </tr>
          </tbody></table>
        </td>
      </tr>
    </tbody></table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="spacer-module" data-muid="vqDDw7scxs521qMEgEyyuF"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">spacer</h4><div class="module-controls-right_1wNFJ"><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="vqDDw7scxs521qMEgEyyuF">
      <tbody><tr>
        <td style="padding:0px 0px 40px 0px;" role="module-content" bgcolor="">
        </td>
      </tr>
    </tbody></table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="social-module" data-muid="811a4d90-5cf8-4edd-afaf-8d7ae129dd7e"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">social</h4><div class="module-controls-right_1wNFJ"><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="editor-social-module_2p3kI"><div class="reset"><table class="module" role="module" data-type="social" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="abc123">
  <tbody>
    <tr>
      <td valign="top" style="padding:0px 0px 0px 0px; font-size:6px; line-height:10px; background-color:#F9F5F2;" align="center">
        <table align="center">
          <tbody>
            <tr align="center">
              <td style="padding: 0px 5px;display:inline-block;" class="social-icon-column">
                <a class="has-url" role="social-icon-link" href="https://facebook.com" target="_blank" alt="Facebook" title="Facebook" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
                  <img role="social-icon" alt="Facebook" title="Facebook" src="https://mc.sendgrid.com/assets/social/white/facebook.png" style="height:30px; width:30px;" height="30" width="30">
                </a>
              </td>
              <td style="padding: 0px 5px;display:inline-block;" class="social-icon-column">
                <a class="has-url" role="social-icon-link" href="https://twitter.com" target="_blank" alt="Twitter" title="Twitter" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
                  <img role="social-icon" alt="Twitter" title="Twitter" src="https://mc.sendgrid.com/assets/social/white/twitter.png" style="height:30px; width:30px;" height="30" width="30">
                </a>
              </td>
              <td style="padding: 0px 5px;display:inline-block;" class="social-icon-column">
                <a class="has-url" role="social-icon-link" href="https://instagram.com" target="_blank" alt="Instagram" title="Instagram" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
                  <img role="social-icon" alt="Instagram" title="Instagram" src="https://mc.sendgrid.com/assets/social/white/instagram.png" style="height:30px; width:30px;" height="30" width="30">
                </a>
              </td>
              <td style="padding: 0px 5px;display:inline-block;" class="social-icon-column">
                <a class="has-url" role="social-icon-link" href="https://www.pinterest.com/sendgrid/" target="_blank" alt="Pinterest" title="Pinterest" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
                  <img role="social-icon" alt="Pinterest" title="Pinterest" src="https://mc.sendgrid.com/assets/social/white/pinterest.png" style="height:30px; width:30px;" height="30" width="30">
                </a>
              </td>
              <td style="padding: 0px 5px;display:inline-block;" class="social-icon-column">
                <a role="social-icon-link" href="" target="_blank" alt="LinkedIn" title="LinkedIn" style="display:inline-block; background-color:#516775; height:30px; width:30px; border-radius:30px; -webkit-border-radius:30px; -moz-border-radius:30px;">
                  <img role="social-icon" alt="LinkedIn" title="LinkedIn" src="https://mc.sendgrid.com/assets/social/white/linkedin.png" style="height:30px; width:30px;" height="30" width="30">
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
  </table></div></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="unsubscribe-module" data-muid="GRteXBNz7UevhwJ6u6GXE"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">unsubscribe</h4><div class="module-controls-right_1wNFJ"><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><div data-role="module-unsubscribe" class="module unsubscribe-css__unsubscribe___2CDlR" role="module" data-type="unsubscribe" style="color:#444444; font-size:12px; line-height:20px; padding:16px 16px 16px 16px; text-align:center;" data-muid="GRteXBNz7UevhwJ6u6GXE"><div class="Unsubscribe--addressLine"><p class="Unsubscribe--senderName" style="font-family:arial,helvetica,sans-serif; font-size:12px; line-height:20px;">{{Sender_Name}}</p><p style="font-family:arial,helvetica,sans-serif; font-size:12px; line-height:20px;"><span class="Unsubscribe--senderAddress">{{Sender_Address}}</span>, <span class="Unsubscribe--senderCity">{{Sender_City}}</span>, <span class="Unsubscribe--senderState">{{Sender_State}}</span> <span class="Unsubscribe--senderZip">{{Sender_Zip}}</span></p></div><p style="font-family:arial,helvetica,sans-serif; font-size:12px; line-height:20px;"><a class="Unsubscribe--unsubscribeLink" href="{{{unsubscribe}}}" style="">Unsubscribe</a> - <a href="{{{unsubscribe_preferences}}}" target="_blank" class="Unsubscribe--unsubscribePreferences" style="">Unsubscribe Preferences</a></p></div></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div><div class="module-wrapper"><div class="module_p3Q6S module" tabindex="0" data-role="spacer-module" data-muid="f5F8P1n4pQyU8o7DNMMEyW"><div class="module-controls_3xpCU"><div><div tabindex="-1" data-role="move" class="module-control_3tr60" draggable="true"><span class="icon-container icon-container_2JZDY"><i class="sg-icon sg-icon-drag sg-icon_3W7YJ sg-icon-drag_3ht3X" tabindex="-1"></i></span></div></div><h4 class="module-type_6EvIR">spacer</h4><div class="module-controls-right_1wNFJ"><div data-role="copy" class="module-control module-control_3tr60"><span data-tooltip="Duplicate" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-copy sg-icon_3W7YJ sg-icon-copy_3mJ4F" tabindex="-1"></i></span></span></div><div data-role="delete" class="module-control module-control_3tr60"><span data-tooltip="Delete" data-tooltip-pos="down"><span class="icon-container icon-container_2JZDY" role="button" tabindex="0"><i class="module-control-icon_lu1RF sg-icon sg-icon-trash sg-icon_3W7YJ sg-icon-trash_Ormn3" tabindex="-1"></i></span></span></div></div></div><div class="module-children_qBvFb"><div class="reset"><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="f5F8P1n4pQyU8o7DNMMEyW">
      <tbody><tr>
        <td style="padding:0px 0px 30px 0px;" role="module-content" bgcolor="">
        </td>
      </tr>
    </tbody></table></div><div class="frame_3gduo"></div></div></div></div><div tabindex="-1" class="drop-area drop-area_2BchA drop-forbidden_1Hjfp"><section class="dropzone dropzone_31DoJ" role="hidden" data-role="module-dropzone" style="align-items: center; display: flex; flex-wrap: wrap; font-size: 14px; justify-content: center;"><div>Drag Module Here</div></section></div></div></div>"""

  message = Mail(
    from_email='cedioza@gmail.com',
    to_emails=email,
    subject=subject,
    html_content=content)
  try:
      sg = SendGridAPIClient(config('KEY_SENDGRID'))
      response = sg.send(message)
      print(response.status_code)
      print(response.body)
      print(response.headers)
  except Exception as e:
      print(e)


# error 404
@app.errorhandler(404) 
def invalid_route(e): 
    return jsonify({'Message' : 'Error 404 Ruta no encontrada intenta nuevamente'})

# error 405
@app.errorhandler(405) 
def invalid_route(e): 
    return jsonify({'Message' : f'Error 405 Metodo {request.method} no esta permitido '})


# Home
@app.route('/home')
def anuncios():
    anuncios=db.reference("/anuncios").order_by_key().limit_to_last(6).get()
    datos=anuncios.items()
    # datos=anuncios.values()
    return jsonify(list(datos))

#Login Usuario

@app.route('/login',methods=['POST'])
def login(): 
  try:  
    data=request.json
    email=data['email']
    password=data['password']
    user=auth.get_user_by_email(email)
    #Validación sí existe usuario 
    if(user):
      usuario=db.reference("/usuarios").child(user.uid).get()
      print(usuario)
      if(usuario["password"]== password):
        token=str(auth.create_custom_token(user.uid,usuario)).split("'")[1]
        return jsonify({"token":token})
      else:
        return jsonify({"Message":"Contraseña Erronea intente nuevamente"})
    else:
      return jsonify({"Message":"Usuario No esta registrado"})
  except :
    return jsonify({"Message":"Datos Incorrectos"})
  # Registro Usuarios

@app.route('/registro',methods=['POST'])
def registroUsuarios():
  reference=db.reference("/usuarios")
  data=request.json
  usuarios={

  "nombre":data["nombre"],
  "typeDoc":data["typeDoc"],
  "numDoc":data["numDoc"],
  "userName":data["userName"],
  "password":data["password"],
  "email":data["email"],
  "phone":data["phone"],
  "state":"1"
  }  
  try:
    if(validarExisteUsuario(reference,usuarios)):
      return jsonify({"Mensaje":"Ya existe un usuario creado con ese cedula"})
    else:
      create=auth.create_user(email=data["email"],password=data["password"])
      reference.child(create.uid).set(usuarios)
      sendEmail(data["email"],data["nombre"],1)
      return jsonify({"Mensaje":"usuario Creado satisfactoriamente","UID":create.uid})
  except auth.EmailAlreadyExistsError:
    return jsonify({"Mensaje":"Ya existe un usuario creado con ese correo"})
    

#Buscar Anuncion
@app.route('/obteneranuncio/<string:uid>',methods=['GET'])
def obtenerAnuncio(uid):
  anuncio=db.reference('/anuncios').child(uid).get()
  alojamiento=db.reference('/alojamientos').child(anuncio["uidAlojamiento"]).get()

  anuncio["telefono"]=alojamiento["telefono"]
  anuncio["email"]=alojamiento["email"]
  anuncioP=[]
  anuncioP.append(anuncio)
   
  return jsonify(anuncioP)

#Crear Anuncio

@app.route('/anuncio',methods=['POST'])
def registroAnuncios():
  try:
    reference=db.reference("/anuncios")
    data=request.form
    imagen=request.files 
    print(data)
    anuncios={
    "nomAnounce":data["nomAnounce"],
    "description":data["description"],
    "numCapacity":data["numCapacity"],
    "location":data["location"],
    "available":"available",
    "uidAlojamiento":data["uid"]
    }

    for i in range(1,len(imagen)+1):
      if(imagen.get(f"file{i}")):
        url=cloudinary.uploader.upload(imagen.get(f"file{i}"))
        anuncios[f"picture{i}"]= url["url"]
    reference.push(anuncios)

    return jsonify({"Mensaje":"Anuncio creado"})
  except Exception as  e:
    reference=db.reference("/error").push(e)
    return jsonify({"Mensaje":"Error creando anuncio"})

#crear un alojamineto con uid enviado


#Documentacion Relacionada Postman
@app.route("/")

def index():
  return jsonify({"Message":"""Ver  solamente 4 anuncios  /home
  Trae todos los eventos /zonaevento """})

#listado de usuarios con credenciales
@app.route('/listadoUsuarios')
def list_usuarios():
  page=auth.list_users()
  data={}
  for user in page.users:
    data={"user": user.uid}
    user
  return (data)

# Obtener todos los  usuarios
@app.route('/usuarios')
def listaUsuarios():
  database = db.reference("/usuarios").get()
  return jsonify(database)

# Obtener usuario en especifico
@app.route('/usuarios<string:uid>')
def listaUsuariosUid(uid):
  database = db.reference("/usuarios").child(uid).get()
  return jsonify(database)


#colocar escuchadores  db.reference('/').listen()
@app.route('/actualizarUsuario',methods=['PUT'])      
def validarActualizarUsuario():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["numDoc"] == data["numDoc"]):
        database.child(key).update(data)
        return True
      else:
        return False   
        
@app.route('/eliminarUsuario',methods=['PUT'])      
def eliminarUsuarios():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["numDoc"] == data["numDoc"]):
        database.child(key).update({})
        return True
      else:
        return False     

#Alojamiento datos con uid dado

@app.route('/registraralojamiento',  methods=['POST'])
def registrarAlojamiento():
  data=request.json
  reference=db.reference("/alojamientos").child(data["userId"])

  alojamiento={
  "nombrealojamiento":data["business"],
  "nit":data["nit"],
  "email":data["email"],
  "telefono":data["phoneBusiness"],
  "responsable":data["manager"],
  "categoria":data["category"],
  "descripcion":data["description"],
  "ciudad":data["city"],
  "direccion":data["address"]
  }
  print(validarExisteAlojamiento(reference,alojamiento))
  if(validarExisteAlojamiento(reference,alojamiento)):
    return jsonify({"Mensaje":"Ya existe un alojamiento  creado con ese nit"})
  else:
    print("ingreso un nuevo alojamiento")
    print(data["userId"])
    reference.set(alojamiento)
    db.reference('/usuarios').child(data["userId"]).update({"state":"2"})
    print("usuario cambio de estado ")
    return jsonify({"state":2})

#lista de productos

@app.route('/actualizarAlojamiento',methods=['PUT'])      
def actualizarAlojamiento():
    database = db.reference("/alojamientos")
    for key, value in database.items():
      if(value["nit"] == data["nit"]):
        database.child(key).update(data)
        return True
      else:
        return False   
        
# mis anuncios en base al uid del anuncio con el parametro del alojamiento


@app.route('/misanuncios/<string:uid>')
def misAnuncios(uid):
  anuncios=db.reference('/anuncios').get()
  anuncioTotalTotal=[]
  try:
    misAnuncios=[]
    anuncioTotal=[]
    if(anuncios):
       for key, value in anuncios.items():
         if(value["uidAlojamiento"] == uid):
           misAnuncios.append(key) 
           data=db.reference('/anuncios').child(key).get()
           anuncioTotal.append(data)
    # for anuncio in misAnuncios:
    #   data=db.reference('/anuncios').child(anuncio).get()
    #   anuncioTotal.append(data)
    #   #  anuncios=db.reference("/anuncios").order_by_key().limit_to_last(6).get()
    #   # datos=anuncios.items()
    #   # # datos=anuncios.values()
    #   # return jsonify(list(datos))
    return jsonify(list(zip(misAnuncios,anuncioTotal)))
  except :
    return jsonify({"Message":"uid incorrecto intente nuevamente" })

@app.route('/eliminarAlojamiento',methods=['POST'])      
def eliminarAlojamiento():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["nit"] == data["nit"]):
        database.child(key).update({})
        return True
      else:
        return False     
# Eventos 

@app.route('/zonaevento')
def zonaEvento():
  eventos=db.reference("/eventos").get()
  return jsonify(eventos)


@app.route('/anuncios')
def zona_anuncios():
  anuncios=db.reference("/anuncios").get()
  datos=anuncios.items()
  return jsonify(list(datos))


@app.route('/evento',methods=['POST'])
def registroEvento():
  reference=db.reference("/eventos")
  data=request.json
  request.headers["nombre de la cabecera "]
  evento={
  "tipoEvento":data["tipoEvento"],
  "descripcion":data["descripcion"],
  "fecha":data["fecha"],
  "hora":data["hora"],
  "numpax":data["numpax"],
  "v_unitario":data["v_unitario"],
  "v_total":data["v_total"],
  "cliente":data["cliente"],
  "alojamiento":data["alojamiento"],
  "proveedor":data["proveedor"]
  }

  if(validarExisteEvento(reference,evento)):
    return jsonify({"Mensaje":"Ya existe un alojamiento creado con ese nit"})
  else:
    create=reference.push(evento)
    return jsonify({"Mensaje":"Alojamiento Creado satisfactoriamente","UID":create.key})

#lista de productos

@app.route('/actualizarEventos',methods=['PUT'])      
def actualizarEvento():
    database = db.reference("/eventos")
    for key, value in database.items():
      if(value["alojamiento"] == data["alojamiento"]):
        database.child(key).update(data)
        return True
      else:
        return False   
        
@app.route('/eliminarEventos',methods=['POST'])      
def eliminarEvento():
    database = db.reference("/usuarios")
    for key, value in database.items():
      if(value["alojamiento"] == data["alojamiento"]):
        database.child(key).update({})
        return True
      else:
        return False     


#metodo validar con una referencia y con una data a almacenar
# retornando true en caso de que si exista 


@app.route('/product')
def product():
  data=db.reference('/product')
  return jsonify(data)

@app.route('/validar')
def validar():
  validar=db.reference('/product').get()
  if(len(validar)>=1):
    for clave in validar:
      if(True):
        print(validar[clave])
        print(len(db.reference('/product').child('-MvqvI_TTUbrDctEB7Ow').get()))
  else:
    validar={"Message":"No hay datos"}
  return jsonify(db.reference('/product').child('-MvqvI_TTUbrDctEB7Ow').get())

# metodos 

  #jsonify(db.reference("/users").child(create.uid).get()) buscamos por el create uid

def validarExisteUsuario(reference,data):
    try:
      database = reference.get()
      if(database):
        for key, value in database.items():
          print(value)
          if(value["numDoc"] == data["numDoc"]):
            return True
      return False
    except :
      return False
def validarExisteAlojamiento(reference,data):
    database = reference.get()
   
    if(database):
      for key, value in database.items():
        if(value["nit"] == data["nit"]):
          return True

def validarExisteEvento(reference,data):
    database = reference.get()
    if(database):
      for key, value in database.items():
        if(value["cliente"] == data["cliente"]):
          return True
        else:
          return False
    else:
      return False

#Correr la Aplicación

# def sendEmail(email):
#   message = Mail(
#     from_email='cedioza@misena.edu.co',
#     to_emails=[email,'flaskemail2022@gmail.com'],
#     subject='Sending with Twilio SendGrid is Fun',
#     html_content="""""")
#   try:
#     sg = SendGridAPIClient(Config("KEY_SENDGRID"))
#     response = sg.send(message)
#     print(response.status_code)
#     print(response.body)
#     print(response.headers)
#   except Exception as e:
#     print(e.body)




if __name__ == '__main__':
    app.run(debug=True)
