from getpass import getpass
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("Welcome to my program, it's a pleasure to see you")

class User:
    def __init__(self):
        print("--------------------------------------------")
        pass

    #fonction servant à enregistrer un nouvel utiisateur
    def create(self):
        while True:
            self.username= input("Your name: ")
            found=self._userConfirm(self.username)#apelle _userConfirm pour pour savoir si le nom est disponible 
            if found:
                print("This username is not available")
            else:
                break


        while True:
            self.userpassword= getpass("Your password: ")
            if len(self.userpassword.strip())<8 or 16<len(self.userpassword.strip()): #le mot de passe doit contnir entre 8 à 16 caractere
                print("Your password must have more than 8 caracters and less then 16 caracter ")
                print("Its for your security")
                continue
            break
        
        masque = "*" * (len(self.userpassword) - 3) + self.userpassword[-3:]# self.userpassword[-3:]// [-3:] recule de trois pas et va jusqu'à la fin
        print(f"Welcome {self.username}, your password ends with {masque}")
        self._save()

    #fonction speciale pour enregistrer dans le compte dans le gestionnaire avec un mot de passe haché
    def _save(self):
        hashed_password = hashlib.sha256(self.userpassword.encode()).hexdigest()#.enconde()= transforme le donné en bites car hashlib travaille avec le bites, .hexdigest()= rend le bite en hexadigit pour une meilleure lecture
        with open("GESTION DE MOT DE PASSE.txt", "a") as file:
            file.write(f"{self.username}:{hashed_password}\n")
    
    
    def login(self):
        self.username= input("What's your username: ")
        found = self._userConfirm(self.username)#apelle _userConfirm pour confirmer si le nom de l'utilisateur est disponible
        if not found:#found= True si le compte existe// False si non// 
            print("Username doesn't exist! Contact your IT support if you already created an account.")
            exit() #si le compte n'existe pas, on sort du programme.
        self.userpassword= self._passwordConfirm(self.username)#cherche le mdp correspondant au username; et le retourne 

        attempts=0
        for i in range(3):#renge(n), n= nombre de tentatives
            pwd= input("Password: ")
            pwd = hashlib.sha256(pwd.encode()).hexdigest()
            if pwd == self.userpassword:
                print("Welcome back "+self.username )
                break
            else: 
                print("You have "+ str(2-i)+ " attempts lef")
                attempts+=1
            if attempts==3:
                print("You have reached the attempt limit")       

    #fonction pour changer le mot de passe
    def reset_password(self):
        self.username = input("Enter your username to reset your password: ")#cherche le compte à reinitialiser
        found = self._userConfirm(self.username)#found= True si le compte existe// False si non//
        if not found:
            print("Username doesn't exist!")
            return
        
        print("Please enter your current password to confirm your identity:")
        current_password = getpass("Current password: ")
        hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()
        self.userpassword = self._passwordConfirm(self.username)

        if hashed_current_password != self.userpassword:
            print("The current password is incorrect!")
            return
        
        print("You can now reset your password.")
        while True:
            self.userpassword = getpass("Enter new password: ")
            if len(self.userpassword.strip()) < 8 or 16 < len(self.userpassword.strip()):
                print("Your password must have more than 8 characters and less than 16 characters.")
                continue
            break
        
        hashed_new_password = hashlib.sha256(self.userpassword.encode()).hexdigest()#hachage du nouveau mot de passe
        self._update_password(self.username, hashed_new_password)#fonction speciale qui ira changer le mdp dans le fichier
        print("Your password has been successfully reset!")
        masque = "*" * (len(self.userpassword) - 3) + self.userpassword[-3:]
        print("Your new password is "+ masque)
    
    #fonction speciale pour confirmer si le compte existe
    def _userConfirm(self, name):
        with open("GESTION DE MOT DE PASSE.txt", "r") as file:
            for line in file:
                if line.startswith(name + ":"):
                    return True
        return False
    
    #fonction spéciale pour renvoyer le mdp correspondant à name
    def _passwordConfirm(self, name):
         with open("GESTION DE MOT DE PASSE.txt", "r") as file:
            for line in file:
                if line.startswith(name + ":"):
                    return line.strip().split(":", 1)[1]
            return None
    

    #fonction speciale qui modifie le mot de passe dans le fichier
    def _update_password(self, name, pwd):
        with open("GESTION DE MOT DE PASSE.txt", "r") as file:
            lines = file.readlines()

        with open("GESTION DE MOT DE PASSE.txt", "w") as file:
            for line in lines:
                if line.startswith(name + ":"):
                    file.write(f"{name}:{pwd}\n")  # Remplace le mot de passe
                else:
                    file.write(line)

#classe coté admin
class Server(User):
    def __init__(self):
        self.login()#appelle login pour pouvoir confirmer la session
    #Rappel que dans login si le compte n'existe pas on fait un exit()


    #fonction pour envoyer le message mail
    def send_confirmation_email(self,receiver_email):

        sender_email = "admin_email_adress" #mail de l'expediteur
        sender_password = "your_email_apps_password" #mot de passe aplication de votre compte gmail, sans espace.

        # Composant du message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Confirmation de création de compte"
        message["From"] = sender_email
        message["To"] = receiver_email

        #contenu du message
        text = f"""\
        Bonjour {self.username},

        Votre compte a bien été créé. 
        
        Merci de nous faire confiance !

        Cordialement,
        IT support
        """
        part = MIMEText(text, "plain")
        message.attach(part)

        # Connexion au serveur SMTP Gmail
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
        except smtplib.SMTPException as e:
            print(f"Erreur lors de l'envoi de l'email: {e}")

#Menu priciapl
u1 = User()
while True:
    choix = input("1. Create account\n2. Login\n3. Reset password\n4. exit\nChoose an option: ")
    if choix == "1":
        u1.create()
    elif choix == "2":
        u1.login()
    elif choix=="3":
        u1.reset_password()
    elif choix=="4":
        break
    else:
        print("Invalid choice.")


u1=Server()
choix= input(f"Do you an email confirmation?(y/o): ")
if choix.startswith("y"):
    mail=input("Your email adress: ")
    u1.send_confirmation_email(mail)


print("Thank for using my first code! <3")
print("Merci d'avoir utilisé mon premier code! <3")
   
