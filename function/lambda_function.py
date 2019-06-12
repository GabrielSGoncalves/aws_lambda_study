import os
import time
from sqlalchemy import create_engine
import smtplib
from validate_email import validate_email
import ssl
import dns.resolver
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# HTML to go on the body of the email
email_content = """
<!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8">
</head>
<body>
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
                     <td style="width:700px;font-family: arial;font-size:20px;color: #000000;text-align: center;line-height:30px;padding-bottom:15px">Entendemos a dificuldade em lidar com os problemas que você pode estar sofrendo, registramos seu interesse, é por vezes é difícil prosseguir.<br>
                        Vamos juntos?!!
                         <br><br>
                        Nossa ferramenta de avaliação foi elaborada com muito cuidado e critérios científicos, não será cobrado nada pelo uso da sugestão diagnostica e o processo leva uns 4 minutos!
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
</body>
</html>
"""


# Main function to be called for lambda
def lambda_handler(event, context):

    # Connect to ClickOn database and execute query on core_clickon table
    db = create_engine(
    'postgresql+pg8000://root:hopes030411@gymbraininstance.c1pkp7hr6szo.us-east-1.rds.amazonaws.com:5432/gymbrain')
    results = db.execute("SELECT * FROM public.core_clickon WHERE points_clickon is NULL")
    print('Getting list of emails from ClickOn Database')
    list_emails = [r.email for r in results]
    

    # Create list to receive emails that are invalid
    invalid_emails = []

    # Iterate over the results from query
    for email in list_emails:
        if r.points_clickon == None:

            # Validate email
            is_valid = validate_email(email, verify=True)

            # Check if email is valid
            if is_valid:
                print('Success! {} is a valid email'.format(r.email))
                
                sender_email = "contato@gymbrain.com.br"
                password = 'Burnoutdepascoa'
                receiver_email = email

                print('Before MIMEMultipart')

                message = MIMEMultipart("alternative")
                message[
                    "Subject"] = "Faça sua avaliação psiquiátrica de forma gratuita"
                message["From"] = sender_email
                message["To"] = receiver_email

                print('After MIMEMultipart')

                # Create the plain-text and HTML version of your message
                # Turn these into plain/html MIMEText objects
                # part1 = MIMEText(text, "plain")
                part = MIMEText(email_content, "html")

                # Add HTML/plain-text parts to MIMEMultipart message
                # The email client will try to render the last part first
                # message.attach(part1)
                message.attach(part)

                print('After message.attach')
                # Create secure connection with server and send email
                context = ssl.create_default_context()

                print('After ssl.create_default_context')

                with smtplib.SMTP_SSL("bh-73.webhostbox.net", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(
                        sender_email, receiver_email, message.as_string()
                    )
                print('END OF LOOP for {}'.format(r.email))

            else:
                print('Email {} does not exist.'.format(email))
                invalid_emails.append(email)

    # Send email to rmiotto@gmail.com and gabriel@codenomics.cloud
    # Define body of email with list of emails
    localtime = time.asctime( time.localtime(time.time()) )
    content = """Segue a lista de emails inválidos acessando o ClickOn:\n
    {}

    Horário de execução do processo: {}
    """.format('\n'.join(invalid_emails), localtime)

    password = 'Burnoutdepascoa'
    message = MIMEMultipart("alternative")
    message["Subject"] = "Teste disparo de emails ClickOn"
    message["From"] = "contato@gymbrain.com.br"
    message["To"] = 'gabriel@codenomics.cloud'
    
    part = MIMEText(content, "plain")

    message.attach(part)

    print('After message.attach')
    # Create secure connection with server and send email
    context = ssl.create_default_context()

    print('After ssl.create_default_context')

    with smtplib.SMTP_SSL("bh-73.webhostbox.net", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

