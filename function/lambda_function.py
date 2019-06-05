import os
from sqlalchemy import create_engine
import smtplib
import email.message

email_content = """
<head>
  <meta charset="UTF-8">
</head>
<table align="center" border="0" cellpadding="0" cellspacing="0" style="width:700px;">
   <tbody>
      <tr>
         <td>
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:700px;">
               <tbody>
                  <tr>
                     <td style="width: 150px;"><img alt="" border="0" src="https://s3.amazonaws.com/transcribe-test-bucket-gymbrain/gymbrain.png" style="display: block;" /></td>

                  </tr>

               </tbody>
            </table>
         </td>
      </tr>
      <tr>
         <td style="height: 250px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:500px;">
               <tbody>
                  <tr>
                     <td style="width:500px;font-family: arial;font-weight: bold;font-size:30px;color: #000001;text-align: center;padding-bottom:15px">Ainda na dúvida sobre a sua situação psiquiátrica?</td>
                  </tr>
                  <tr>
                     <td style="width:700px;font-family: arial;font-size:20px;color: #000000;text-align: center;line-height:30px;padding-bottom:15px">Sabemos da dificuldade em lidar com os problemas que você pode estar sofrendo e queremos muito ajudá-lo a superá-los. 
                         <br><br>
                        Nossa ferramenta de avaliação psiquiátrica é grátis e o processo não dura 4 minutos.
                        <br><br>
                        Acesse através do <a href="https://appgymbrain.com"><b>link</b></a> e nós da GyMBrain teremos o prazer em ajudá-lo com o que há de mais avançado em diagnóstico psiquiátrico.
                        <br><br>
                        <a href="https://appgymbrain.com"><b>Saiba mais a repeito!!</b></a><br><br>


                  </td>
                  </tr>
                 
               </tbody>
            </table>
         </td>
      </tr>
      <tr>
         <td style="background-color: #1C6D98;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:600px;">
               <tbody>
                  <tr>
                     <td style="width: 258px;"><img alt="" border="0" src="http://www.hnehealth.nsw.gov.au/hnet/PublishingImages/Pages/Hunter-New-England-Training-in-Psychiatry-%28HNET%29/Registrar%20Brain%20Photo.JPG" style="display: block;" /></td>
                     <td style="width: 342px;">

                     </td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>

      <tr>
         <td style="background-color: #B0D154;padding-top:22px;padding-bottom:22px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:536px;">
               <tbody>
                  <tr>
                     <td align="right" style="width: 68px;font-family: arial;font-size:13px;color: #ffffff;text-align: right;line-height:13px;">Siga-nos:</td>
                     <td style="width: 146px;">
                        <table align="center" border="0" cellpadding="0" cellspacing="0" style="width:120px;">
                           <tbody>
                              <tr>
                                 <td align="center"><img alt="" border="0" height="15" src="http://emailmarketingtemplates.com.br/templates/newsletter/business-4/Business-4_7.png" style="width:15px; height:15px;" width="15" /></td>
                                 <td align="center"><img alt="" border="0" height="15" src="http://emailmarketingtemplates.com.br/templates/newsletter/business-4/Business-4_6.png" style="width:15px; height:15px;" width="15" /></td>
                                 <td align="center"><img alt="" border="0" height="15" src="http://emailmarketingtemplates.com.br/templates/newsletter/business-4/Business-4_9.png" style="width:15px; height:15px;" width="15" /></td>
                                 <td align="center"><img alt="" border="0" height="15" src="http://emailmarketingtemplates.com.br/templates/newsletter/business-4/Business-4_8.png" style="width:15px; height:15px;" width="15" /></td>
                              </tr>
                           </tbody>
                        </table>
                     </td>
                     <td align="right" style="width: 322px;font-family: arial;font-size:13px;color: #ffffff;text-align: right;line-height:13px;"><a href="http://gymbrain.com.br" style="color: #ffffff;text-decoration: none;"> gymbrain.com.br</a></td>
                  </tr>
               </tbody>
            </table>
         </td>
      </tr>
   </tbody>
</table>
"""


def lambda_handler(event, context):
    var1 = os.environ.get("var1")
    var2 = os.environ.get("var2")

    db = create_engine(
        'postgresql+pg8000://root:hopes030411@gymbraininstance.c1pkp7hr6szo.us-east-1.rds.amazonaws.com:5432/gymbrain')
    results = db.execute("SELECT * FROM public.core_clickon")
    for r in results:
        if r.points_clickon == None:
            print(r.email)
            server = smtplib.SMTP('smtp.gmail.com:587')
            msg = email.message.Message()
            msg['Subject'] = 'Teste Python Email HTML'

            msg['From'] = 'gabrielgoncalvesbr@gmail.com'
            msg['To'] = r.email
            password = "atlas2000"
            msg.add_header('Content-Type', 'text/html')
            msg.set_payload(email_content)

            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()

            # Login Credentials for sending the mail
            s.login(msg['From'], password)

            s.sendmail(msg['From'], [msg['To']], msg.as_string())
