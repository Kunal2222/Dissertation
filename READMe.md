<<<<<<< HEAD
﻿

University of Sheﬃeld

Using Machine Learning of User

Keystrokes to Identify Hijacked Sessions

Kunal Das

Supervisor: Andrew Stratton

A report submitted in fulﬁlment of the requirements

for the degree of MSc in Cybersecurity and AI

in the

Department of Computer Science

September 14, 2022





Declaration

All sentences or passages quoted in this report from other people’s work have been speciﬁcally

acknowledged by clear cross-referencing to author, work and page(s). Any illustrations that

are not the work of the author of this report have been used with the explicit permission

of the originator and are speciﬁcally acknowledged. I understand that failure to do this

amounts to plagiarism and will be considered grounds for failure in this project and the

degree examination as a whole.

Name: Kunal Das

Signature: Kunal Das

Date: 14/09/2022

i





Abstract

Security is one of the most important concerns of modern society. As a result of concerns

about their data, individuals and companies are striving to improve authentication techniques.

Secure passwords are adopted by modern society, and two-factor authentication is implemented

by most businesses. What is the next step? By implementing continuous authentication,

these two problems can be addressed from both sides. There is no need for users to be

concerned about their active login session. By securing their services more widely and

protecting themselves from automated attacks, companies can increase the level of security

for their services.

The purpose of the project is to develop an eﬀective application for detecting a non-legitimate

user acting like a genuine user to prevent this kind of spooﬁng attack automatically. While a

user is typing the system. Aim to obtain some new information rather than merely reiterating

previous ﬁndings. An authentication method based on password typing keystroke dynamics

has been previously developed. Based on the results, the system will decide whether or not to

make the session active. Here is the goal to capture writing data and validate that for the user.

As a result, future versions of this software might be able to authenticate any device with the

use of other features. A web application can include mouse dynamics along with keystroke

dynamics. In this work, user identiﬁcation is the main objective that has been achieved by

writing patterns. In addition, users are now able to leave their work whenever they wish, and

when another user begins to use the system the session will be closed by the system. A shell

script authentication system will also be available in the near future. By implementing this

methodology, server attacks can be reduced. Active sessions can save users time and eﬀort

by reducing the need to enter passwords or use 2FA every time.

ii





Contents

1 Introduction

1

1

2

1.1 Aims and Objectives . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

1.2 Overview of the Report . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2 Literature Survey and Background

4

4

5

5

6

7

7

8

8

8

9

9

9

2.1 Authentication . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.1.1 Password Authentication . . . . . . . . . . . . . . . . . . . . . . . . .

2.1.2 Two-Factor Authentication . . . . . . . . . . . . . . . . . . . . . . . .

2.1.3 Biometric Authentication . . . . . . . . . . . . . . . . . . . . . . . . .

2.1.4 Token Authentication . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.1.5 CAPTCHA . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.2 Languages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.2.1 HTML . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.2.2 CSS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.2.3 JavaScript . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.2.4 Python . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.3 Use of Artiﬁcial Intelligence (AI) in Real Time Application . . . . . . . . . .

2.3.1 Navigation System . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10

2.3.2 Language Processing Applications . . . . . . . . . . . . . . . . . . . . 10

2.4 Machine Learning . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10

2.4.1 Supervised Learning . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11

2.4.2 K-Nearest Neighbors . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

2.5 Continues Authentication . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 15

2.5.1 Keystroke Dynamics . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16

3 Implementation and Analysis

20

3.1 Design . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 20

3.1.1 Front-end . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

3.1.2 Back-end . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22

iii





CONTENTS

iv

4 Results

36

4.1 Performance Measure of KNN . . . . . . . . . . . . . . . . . . . . . . . . . . . 36

4.1.1 Keystroke Patterns . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37

4.1.2 Confusion Matrix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 38

5 Conclusions and Future Work

42





List of Figures

2.1 Simple Authentication . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.2 Password Authentication . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.3 Two-Factor Authentication . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.4 Biometric Authentication . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.5 Token Authentication . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

2.6 CAPTHA . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

4

5

6

6

7

8

2.7 Supervised Learning for label based training . . . . . . . . . . . . . . . . . . . 11

2.8 Regression . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

2.9 K-Nearest Neighbors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

2.10 K-Nearest Neighbors with New Instance . . . . . . . . . . . . . . . . . . . . . 14

2.11 Keystroke Authentication Process . . . . . . . . . . . . . . . . . . . . . . . . 17

3.1 Registration Page . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

3.2 Login Page . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21

3.3 Home Page . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22

3.4 Logout Page . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22

3.5 Secret Key . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22

3.6 Session Key . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23

3.7 Registration Back-end . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24

3.8 Secuirty Function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25

3.9 Authentication Function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 26

3.10 Key Example . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27

3.11 Keystroke Collection Process . . . . . . . . . . . . . . . . . . . . . . . . . . . 28

3.12 Feature Extraction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30

3.13 Feature Extraction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30

3.14 Data Flow Diagram . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31

3.15 Data Collect . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32

3.16 Normalization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33

3.17 Training Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34

3.18 Prediction Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35

4.1 Keystroke Patterns of two user . . . . . . . . . . . . . . . . . . . . . . . . . . 38

v





LIST OF FIGURES

vi

4.2 Genuine Matrix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39

4.3 Imposter Matrix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39

4.4 JSON Data Structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 40

4.5 Authentication Writing UI . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41





List of Tables

2.1 Spam and Ham Data Sample . . . . . . . . . . . . . . . . . . . . . . . . . . . 11

2.2 Used Car Data-Set . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

2.3 User Typing Characteristics . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16

2.4 Classiﬁer Comparison with 2009 Databse . . . . . . . . . . . . . . . . . . . . 19

3.1 Keystroke Dataset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29

4.1 Genuin User Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 36

4.2 Imposter Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37

vii





Chapter 1

Introduction

Nowadays, people are increasingly dependent on technology. The physical card people use is

also not fully identiﬁed that this is the genuine user. In every application from an online store

to banking or social media. The Internet is a necessity for most people. People started storing

their data on online cloud storage (Siddiqui et al., 2021). Hackers can also gain access to

local WiFi networks. Passwords and accounts can be hacked by external or Internal hackers

(Killourhy and Maxion, 2009). The companies implemented authentication methods in order

to ensure that the network and web-based applications were secure. In order to implement

biometric features, it is very expensive. A further disadvantage of biometrics is that it does

not have the capability of continuously authenticating a person. A building or other location

can be accessed by anyone by using another person’s key card, just as in movies. It can be

a serious problem if someone gets access to someone else’s account without their consent.

There is also the possibility that people sometimes lose their phones and then someone else

is able to use them. In situations like these, it would be helpful to add an additional layer

of security. Keyboard and mouse usage can be a biometric feature for users. It will require

less data to be authenticated. It can be used in future for online behavioral authentication

schemes. For security-sensitive apps, continuous authentication is critical. A session can be

attacked in several ways like a Man-in-the Middle (MITM) attack where an attacker can

steal the session key between a server and client. After that they can access the system later.

The user will know the information after the breaking. By that time there may be some

changes already that can not be revoked. Spooﬁng attacks can be prevented by continued

authentication (Siddiqui et al., 2021).

1.1 Aims and Objectives

In the project, the aim was to develop an application that would detect whether or not a

user is authentic. Prior research has revealed a number of challenges related to data being

able to change based on physical equipment or being unstable during the collection of data.

It is possible for a coat to slow down hand movements or a scratch on a ﬁnger make typing

slower than usual. When someone wears gloves, that will result in a diﬀerent pattern for

1





CHAPTER 1. INTRODUCTION

2

learning. In the real world, there will be several challenges. According to previous research,

researchers initially analyzed user keystrokes for two features. 1% of the results were accurate.

In the past, a variety of machine learning algorithms have been used. Random Forest, Neural

Networks, K-Means, KNN but K-Nearest Neighbor gives the best result in every research.

So, KNN has chosen to implement this application. KNN distance metrics help to generate

clusters. Cluster is a chuck of a dataset which is explained further in this paper. Several

distance metrics are used in the past research papers like Manhattan, Euclidean, Minkowski

and others. As part of this paper, these distances are also explained. The last timing was

5 minutes and in this application the target was 3 minutes to detect the user. For this

particular topic always the aim will be time consideration.

1.2 Overview of the Report

An application has been developed for the project. The project developed on HTML, CSS,

JavaScript and python. Several libraries used to develop the application. It is important to

note that Python ﬂask serves as the main framework for balancing the project architecture.

The application was developed with several front-end pages. The application generates data

which is stored in an online database called MongoDb. In chapter 2, several authentication

methods are discussed, from basic authentication to biometric authentication. It is also

necessary to be aware of the bugs in the system so that the problem can be ﬁxed from all

angles. To use the secured login process, a registration form is created for new users and

a login page is created for existing users. For pattern learning, Machine Learning uses the

K-Nearest Neighbors algorithm to distinguish between real and fake users. Browser-based

interval-based data collection. The browser sends the data to the server at regular intervals.

AJAX is essential to making an interactive client-server interface. Data was collected by

counting the interval between key entries using timestamps. This program measures the time

between pressing two keys or releasing two keys. For the generation of a shared key, a key

exchange procedure is also employed. This encryption is based on NIST P-256. During the

diﬃe hellman key exchange between a server and a client, the procedure is carried out. An

encrypted password is assigned to the secret, which will be used to create a session key. In

order for a browser to be secure, dynamic key exchange is not necessary. Using dynamic secret

keys in ﬂask will prevent the session key from being stored. Sessions will be cleared every

time they are refreshed. If someone logs out of the web application, they can’t log in again

without their username and password. Flask handles navigation in the web application. Two

research backgrounds were selected for the project to discuss where both research conducted

on password typing characteristics. In 2009, more than 100 users were surveyed for the last

research study. As part of the evaluation of the performance of new distance matrices, the

same dataset was used. The following set of data was collected from users who manually

entered text into a text ﬁeld to generate the data. It should be noted, however, that data

is the primary concern in this area for every research. This has been the case in the past

when researchers have applied their models to the dataset. However, they did not develop a





CHAPTER 1. INTRODUCTION

3

software application to facilitate password typing. It may be helpful, however, if the model is

capable of detecting a good level of accuracy. Future research will focus not only on keystroke

dynamics, but also on mouse and smart phone touch sensitive data. During the collection

of data, some challenges were also encountered. Data can be aﬀected by changes in user

behavior resulting from fast or slow typing speeds.





Chapter 2

Literature Survey and Background

2.1 Authentication

An authenticating process involves verifying the identity of an authorised individual or thing.

The purpose of authentication is to prove the authenticity of something which was made by

a person or a person or an incident in history. Dealing with security is a common problem

in every ﬁeld. In practice, authentication can be performed by testimony, identiﬁcation

documents, or when the authenticator already knows the individual or thing (Contributors,

2019). In Fig. 2.1 , the ﬁgure shows examples of authentication processes in diﬀerent

locations. A security check at an airport is illustrated in Example 1. Security reasons require

airport authenticators to ensure that travellers do not carry any harmful things or devices.

Example 2 illustrates how ID cards are used as identity cards throughout any organisation.

Authenticators will not allow it without the ID card or if the person’s details do not match

in their existing database if they forgot it. In the last example, we check the validity of car

number plates.

Figure 2.1: Simple Authentication

4





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

5

2.1.1 Password Authentication

The password authentication process is straightforward to follow. When using password

authentication, usernames and passwords are critical considerations. Access to a system or

website will be granted if the inputs are correct. There are times when users use unsecured

passwords like ’password’, ’abcdefg’,’12345’ etc. There is a high probability of cracking or

guessing these passwords. It is common for hackers to use programs to decrypt passwords.

If the password is simple, it will be much easier for the hacker to gain access to the account.

Now, programmers are striving to make sure that the system is secure and that users are

not able to access any simple passwords. The minimum length is usually 8 digits, with

uppercase letters, lowercase letters, numbers, and special characters mandatory on most

websites (N-Able, 2019).In Fig. 2.2, an authorised user must enter a username and password

in order to access the system. The use of password authentication is common practice on

all electronic devices and software’s, including smartphones, tablets, computers, and most

websites. Occasionally, websites set an expiration date for passwords, and users need to

change their passwords before or on that date. Users with old passwords may be unable to

reset their passwords in the system.

Figure 2.2: Password Authentication

2.1.2 Two-Factor Authentication

Two-factor authentication is similar to password authentication, except it involves the use

of a physical device registered by the user or provided by the organisation where the user

is registered. A one-time password (OTP) is sent to the user when he or she enters their

username and password, or through the use of an authenticator app generates a pass-code

or approves a notiﬁcation sent by the system when the user attempts to log in. Using the

second authentication method will prevent someone from accessing the system if they already

know the password. A number of examples can be found in our daily lives, such as ATM’s.

ATM withdrawals require the user to simultaneously use their debit card and pin (N-Able,

2019). In Fig. 2.3, it is shown in the ﬁgure that the same process is used for logging in as

with normal password authentication, but with an added layer of security. The user receives

a text message with a one-time password (OTP) that enables them to successfully log into

their account after entering the OTP.





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

6

Figure 2.3: Two-Factor Authentication

2.1.3 Biometric Authentication

Biometric authentication is one of the most secure authentication methods available. In order

to authenticate a person, physical features are required. An individual may authenticate by

using his or her face, retinal scan, voice or ﬁngerprint. For a legitimate user, it is very

diﬃcult to break or pass this authentication. This authentication method has the advantage

that users do not have to remember usernames or passwords, nor do they have to carry any

cards or devices in order to authenticate. Occasionally, devices such as phones, laptops and

tablets are unable to authenticate a particular feature, such as ﬁngerprints and retinal scans.

In order to accomplish this, companies use special devices. It is not uncommon for users

to refuse to share their physical characteristics or identities with companies or government

agencies unless they have a legitimate reason to do so (N-Able, 2019).

Figure 2.4: Biometric Authentication





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

7

2.1.4 Token Authentication

In some cases, companies do not want to use cell phones or rely on any other authentication

layer (N-Able, 2019). Hardware and software are both involved in token authentication

(inwedo, 2022). The token authentication process is built to support two-factor authentication.

In place of a cell phone, companies oﬀer smart cards or USB tokens (N-Able, 2019), which

must be used with a card reader or USB port in order to operate (inwedo, 2022). Cards like

RFIDs with radio frequency communication and USB dongles . The use of authentication

devices also requires users to be cautious in order to prevent their use by unauthorised

individuals (N-Able, 2019). Unlike hardware tokens, software tokens are not visible and

can be used by any electronic device, including smartphones, tablets, laptops, etc (inwedo,

2022).In Fig. 2.5, this ﬁgure illustrates two examples. One is hardware that uses RFID

technology. Once a RFID tag is placed near an antenna, the antenna communicates with

the RFID tag and activates an electric current to unlock the door. An example of server

authentication is shown in the second illustration, in which the user logs in and a token of

authentication is generated from the authentication server, and based on that token, the user

receives the data from the resource server.

Figure 2.5: Token Authentication

2.1.5 CAPTCHA

Automated attacks are increasingly being made by hackers in an eﬀort to gain access to the

system. The use of captcha is eﬀective in preventing this type of attack. As opposed to

detecting an automatic attack, it focuses on verifying an actual human is attempting to use

the service. By using numbers, pictures and letters in a diﬀerent format, captcha attempt

to generate a unique identiﬁer that only a human is capable of deciphering and not only.





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

8

Although it provides an additional layer of security against hackers, it only causes problems

for disabled individuals such as blind individuals in auditory screen readers. The captcha are

inaccessible to them. It is not uncommon for non-disabled users to encounter some diﬃculty

in solving captcha (N-Able, 2019).In Fig. 2.6 (okta, 2021) this section, you will ﬁnd some

examples of captchas that are used to authenticate users.

Figure 2.6: CAPTHA

2.2 Languages

2.2.1 HTML

The HTML language is used for the distribution of information worldwide. The language is

understandable globally. In addition to being understandable by most computers, it is also

used for computers to publish content. The language known globally as HTML is used by

the World Wide Web (WWW). HTML stands for Hypertext Markup Language. Publishing,

data, media content, ﬁles, and ﬁnding information online are all made easier by HTML. It was

originally developed by Tim Berners-Lee. After authors and vendors began using HTML in

the same way, HTML started expanding in diﬀerent directions. The development is boosted

by a joint eﬀort between diﬀerent organisations. There is now a version 5 of HTML available.

This mechanism changed in various ways, such as developers now being able to use style

sheets, scripting, frames, embedding objects, as well as improving accessibility for persons

with disabilities (Raggett et al., 1999).

2.2.2 CSS

Contents published in HTML can be designed with CSS (Cascading Style Sheets). Published

documents are presented in an attractive way using this technique. HTML without CSS

looks like a basic designed page. It has become critical for companies to develop front-end

development strategies to attract or maintain meaningful information for their customers





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

9

(Meyer, 2006). The CSS 4 standard is currently available. In addition, it oﬀers a dynamic

interactive option using JavaScript or some JavaScript libraries such as AJAX and jQuery.

In addition to allowing the user to change the colors, spacing, borders, and dimensions, there

is also the option of adding animation and transformation. In order to make the libraries

more dynamic, some features have already been added (Nixon, 2014).

2.2.3 JavaScript

For web browsers, JavaScript is an important language. As a result of its integration with

browsers, it has become the most popular language. It was after the failure of JavaTM

applets that JavaScript was introduced on its own to the industry. Aside from that, many

programmers consider it to be a distasteful language as well. The majority of people do not

learn JavaScript because if they wish to develop something in an environment which only

supports JavaScript, they will choose to learn an alternative language which can be supported

in most of the environment. Since JavaScript is an easy-to-learn language, it can be used by

anyone. It also supports object-oriented programming, so users can structure data based on

objects and store them as JSON ﬁles (Crockford, 2008).

2.2.4 Python

Python was developed approximately in 1991. In other words, it is an interpreted language

(Python, 2021). A program is executed by an interpreter, which is why it’s called an

interpreted language (Downey, 2012). Python covers a wide range of areas including procedural,

functional and object-oriented programming. It is inspired by diﬀerent programming languages,

including C, Java, Lisp, and Haskell (Python, 2021).The Python programming language

optimizes the accuracy, performance, integration, eﬃciency and of the system. In addition to

product design, web development, user interfaces and system programming, it is now used for

a variety of tasks. As a result of its ease of implementation, Python is often called a scripting

language (Van Rossum and Drake Jr, 1995). As a result of its ease of implementation,

Python is often called a scripting language. As well as that, it has the fastest expansion rate

in the world. Developers are able to learn and implement machine learning with the help of

well-designed packages (Vallat, 2018).

2.3 Use of Artiﬁcial Intelligence (AI) in Real Time Application

The purpose of artiﬁcial intelligence is to act like a human and to assist humans in their daily

activities. Artiﬁcial intelligence is the combination of a number of methodologies, including

deep learning and machine learning (Javatpoint, 2021). In everyday life, people use AI for a

variety of applications. In addition to being used in diﬀerent domains for diﬀerent purposes,

the improved version of the applications is able to perform correct calculations and process

large data with accurate results. Maps, social media, search engines, banks, and marketing

are just a few examples of industries. AI has become dominant in every ﬁeld.





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

10

2.3.1 Navigation System

Most of the people depend on google maps. People ﬁnd it useful to ﬁnd new places easily.

Previously maps used online satellite navigation to guide users. As a result of AI, now a user

not only has a better experience, but also has the opportunity to see surroundings. The use

of image processing to recognize handwriting labels is also helpful for users to ﬁnd their exact

location. An application that understands traﬃc and learns about it. Users can then choose

the best route for their journey based on that information (Javatpoint, 2021).

2.3.2 Language Processing Applications

There are times when users have diﬃculty typing an email or sending a message to someone.

Sometimes people forget to correct typing mistakes. In addition to preventing this mistake,

AI helps recommend keywords that can help users write in a better way and provides a writing

tone that the user is trying to achieve. The process of learning a new language requires a lot

of patience. In the model, the data feed helps to identify mistakes and show them in colored

markings. Additionally, it makes learning easier for users. The use of language processing can

help users solve their problems in other ways as well. Frequently, users encounter diﬃculties

getting answers for a speciﬁc product or service and they try to get instant solutions at that

moment. They may have to wait for someone to assist them in person or over the phone.By

the help of AI complex questions can also be answered online with the assistance of chat bots.

Users received good recommendations online for their searches. The majority of the time,

they are able to locate the answer or information that the user was looking for (Javatpoint,

2021).

2.4 Machine Learning

Programming techniques based on machine learning aim to learn from data sets. Typical

daily mail systems receive a large number of emails, including spam. Whenever a user marks

an email as spam, the machine learning model learns that, and marks unmarked or regular

emails as ham. Data records such as these can be used to train a machine learning algorithm.

The training process is considered as an instance (G´eron, 2017).

To learn and categorise the data, machine learning uses a variety of systems. Human

supervision is provided during the implementation of the methods. A number of methods are

available, including supervised, unsupervised, semi-supervised, and reinforcement learning.

The learning of systems can be done online or in batches. In the system, data points are

compared with previous data or identify patterns and develop models to predict the outcome.

It is not necessary to use all criteria. Depending on the requirements or desired outcome,

Machine Learning can be customised in any way. It is possible to classify machine learning

based on supervision and time provided during training (G´eron, 2017).





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

11

2.4.1 Supervised Learning

In supervised learning, the data collected for the training already have the result and it is

called labels. A supervised learning program is a classiﬁcation program. In Fig. 2.7 (G´eron,

2017), showing the example of email trained with classes of spam and ham email and try to

predict the result for a new instance. Emails should be classiﬁed by the system as they are

received (G´eron, 2017).

Figure 2.7: Supervised Learning for label based training

The number of indicated words or characters is equal to the number of words or characters

in an email. The example in Table 4.1 illustrates the diﬀerence between spam and ham in

words and characters (Hastie et al., 2009).

george you your hp

free hpl

!

our

re

edu remove

spam

ham

0.00

1.27

2.26 1.38 0.02 0.52 0.01 0.51 0.51 0.13 0.01

1.27 0.44 0.90 0.07 0.43 0.11 0.18 0.42 0.29

0.28

0.01

Table 2.1: Spam and Ham Data Sample

In order for the prediction model to learn, the data is collected. As a result of learning, an

outcome can be predicted for unknown data. A good learning process will produce accurate

results. Using the example, we can see how supervised learning works. The term supervised

name is derived from label guidance learning. Previously, a study was conducted to predict

whether emails would be classiﬁed as junk mail or not. This project was designed to detect

and judge whether an email should be categorised as spam for the user or not. 4601 email

messages were used for training and classiﬁed as spam or email (legitimate user). According

to the analysis of the research, 57 words and punctuation’s appear frequently. This problem





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

12

falls under the category of supervised learning. An example of a classiﬁcation problem is a

problem with labels attached to spam/email.

For another example. It is possible to measure the price of some items based on their features.

Predictors like age, brand, and mileage are used for cars. Regression is a technique for sorting

tasks. Various car samples with diﬀerent features are needed for the analysis. Mileage may

be deﬁned diﬀerently for machine learning purposes. You can use the feature for diﬀerent

purposes in diﬀerent circumstances. In this case, it is denoting a numerical value. Despite

the fact that attributes and features are often used equally. Regression can also be used as

a classiﬁer sometimes. The logistic regression method, for example, is most often used as a

classiﬁer (G´eron, 2017).

Figure 2.8: Regression

2.4.2 K-Nearest Neighbors

The KNN algorithm is a type of supervised learning algorithm. That has been developed for

the purpose of data mining and machine learning. It is an example of classiﬁcation, where it

compares past and present data using vectors. In terms of algorithms, KNN is a simple one.

This Table 2.2 (kaggle, 2020) illustrates how a database can be fed into a machine learning

model to predict a new used car price. The machine learning algorithm predicts a new price

based on the similar features in the used cars dataset. Each type of combination refers to

the price of each individual vehicle. The price of any car can be predicted by using each row

of data as a classiﬁcation. In the case of a car purchased in 2012 with 80000 kilometres of

mileage, the model will attempt to ﬁnd the closest matching set of data and estimate the

price (Jos´e, 2018).





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

13

brand model

focus 5 Series

focus 6 Series

focus 5 Series

focus 1 Series

year price transmission mileage tax mpg engineSize

2014 11200 Automatic

2018 27000 Automatic

2016 16000 Automatic

2017 12750 Automatic

2016 11000 Manual

2017 16800 Automatic

2019 17300 Manual

2016 13900 Automatic

2016 13250 Automatic

2016 11750 Manual

2015 10200 Manual

2017 10550 Manual

67068

14827

62794

26676

29946

25952

1998

125 57.6

145 42.8

160 51.4

2

2

3

145 72.4 1.5

30 55.4 1.4

audi

audi

audi

audi

audi

audi

audi

A1

A4

A3

A1

A6

A4

A3

145 67.3

145 49.6

2

1

32260

76788

75185

46112

25250

1264

30

30

20

20

58.9 1.4

61.4

70.6

2

2

60.1 1.4

skoda Octavia

skoda Citigo

skoda Octavia

150 54.3 1.4

2018 8200 Manual

2019 15650 Automatic

145 67.3

145 67.3

165 51.4

1

2

2

6825

skoda Yeti Outdoor 2015 14000 Automatic

skoda Superb 2019 18350 Manual

skoda Yeti Outdoor 2017 13250 Automatic

28431

10912

47005

150 40.9 1.5

145 51.4

2

Table 2.2: Used Car Data-Set

KNN follows distance measurement algorithms like Euclidian, Manhattan, Minkowski. Where

these formulas help to ﬁnd the labels for prediction. Where in 2.1 euclidean distance p and

q measure as two points in Euclidean n-space. Each side of the triangle is calculated by

subtracting one point from another point in every dimension. Add the squared result to the

total. Finally, the square root of that measurement represents the Euclidean distance. For

2.2 Manhattan distance, sum all absolute diﬀerences between all dimensions between any two

points.Where n is number of dimensions. Two dimensions are used to represent Manhattan

distance. The 2.3 Minkowski distance metric can be deﬁned as the generalisation of the

distance metric across an normed space of vectors. It is simply a generalisation of Euclidean

and Manhattan distances (Jos´e, 2018).

v

u

Xn

u

t

d(P, Q) =

(q − p )2

(2.1)

i

i

i=0

Xn

d(P, Q) =

|p − q |

(2.2)

(2.3)

i

i

i=1



!

1

c

Xn

c

d(X, Y ) =

(|x − y |)

i

i

i=1

An instance of a cluster is generated by a KNN model in Fig. 2.9. The colours of each cluster

correspond to the cluster in which they belong. It is possible for clusters to be scattered if

classiﬁcation is complicated or overlapped.





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

14

Figure 2.9: K-Nearest Neighbors

According to Fig. 2.10, it will show the distance between clusters based on the value of k. If

k is 3, the distance between the 3 clusters closest to it will be calculated. In the ﬁgure, the

circle around 3 classes represents the nearest 3 clusters. Assuming k = 8, it will calculate

distances for the 8 nearest classes as shown in the graph. The prediction for the three classes

is blue since the blue number class received the most votes. As the result of a value of 8 is

orange, the result is due to the fact that it received four votes (Jos´e, 2018).

Figure 2.10: K-Nearest Neighbors with New Instance





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

15

2.5 Continues Authentication

The authentication of authorised users poses one of the biggest problems in implementing

secure systems. In our real-world application, password authentication or two-factor is

available. New implementations are essential to getting stronger authentication. In the

ﬁrst level of security, strong passwords or strong encryption methods have already been

developed along with encrypted communications. Authentication devices are more expensive

or have a much higher risk of being lost. One of the strengths will be being able to develop

something that can’t be transferred like hardware devices or diﬃcult to understand. The

implementation of biometric authentication requires a substantial budget. Small businesses

cannot aﬀord it or mid-sized businesses ﬁnd it diﬃcult. The implementation process can also

be lengthy and cannot be updated easily with new technology. It is feasible to implement

low-cost authentication techniques such as continuous authentication on a low budget and

to authenticate without requiring the user to provide any personal information. Analysing

handwritten letters with their previous letters is similar to this process. The system should

detect whether the user is acceptable or not. The system can prevent potential damage

caused by imposters. The detection of imposters in less than 100 words had already been

studied in a previous experiment. A slight change or temporary diﬃculty can change the

typing pattern. It is possible, for instance, for a user to use his coat to ﬁll up a heater in a

cold room. Typing speed may slow down when a hand moves slowly due to a coat, or changes

may occur in writing pattern. For the purpose of identiﬁcation, Keystroke characteristics are

crucial. A unique digital print is created by the time interval between keys. Also the error

frequency can be tracked for authentication. Keystroke force, typing rate and text statistics

also can be a helpful feature with Keystroke timings. A key rollover and key lockout system

is already built into the keyboard hardware. The most natural typing can be done with these

facilities. In the absence of it, the user may need to press one key at a time, which may

result in slower performance. A single key is pressed and another is pressed before releasing

or after a few milliseconds, handled by key rollover. If a key is repeatedly pressed, the data

can be aﬀected, which can be dealt with by a key lockout that eliminates that particular key

data (Shepherd, 1995).

There are times when the keyboard hardware interrupts for key presses and releases. A

hardware scanner identiﬁes the key codes from key press or release actions, which are then

processed by the system for identiﬁcation. Most of the information is lost after data is

transmitted to the BIOS. As an example, the capital key is not valid unless you press the

shift key. This is why alt, ctrl, and shift keys provide left-handed and right-handed users with

two options on the left and right side of the keyboard. In BIOS, both sides produce the same

results. No matter which way it is pressed, the system discards it. That is not the logical

part. The time of each key is recorded and it is known as the key input handler. By using

the system, the keystroke interval and overlap are calculated. In the past, an application

using Turbo Pascal was developed. In order to analyse keystroke logs, these systems utilise

TSR. The application was based on PASSWORD typing detection and required a password





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

16

input 5 times. The stats generated from duration of individual keys and duration. Then they

calculated the mean and variance. The authorization will be based on these measurements

(Shepherd, 1995).

The measurement is accurate to within 1%. The challenges were related to timing. The

data was aﬀected by long pauses. As a result of breaks, the system was suspended in order

to stop calculating means and variances. Data from four users was presented as an example

in Table 2.3. Two of them were professionals and their typing rate per second was similar

but learned from diﬀerent people. The third user was not a professional typer but a frequent

keyboard user. An irregular individual was present in the fourth case (Shepherd, 1995).

Duration

User Mean Var

66ms 12ms 122ms 18ms

59ms 8ms 104ms 22ms

Interval

Mean Var

1

2

3

4

81ms 20ms 225ms 140ms

102ms 34ms 665ms 320ms

Table 2.3: User Typing Characteristics

In Table 2.3, the professional user strikes 6 keys per second, that’s 60 words per minute with

an average of 6 letters per word. In addition to the keystroke durations being diﬀerent, the

durations were also remarkably diﬀerent. It takes the third user longer to ﬁnd keys than it

does for the professionals. The fourth and last user is demonstrating the typing experience

by comparing data with others.

2.5.1 Keystroke Dynamics

A second study was conducted on authentication. Based on novel keystroke dynamics

authentication for industrial use. Where a system can detect a non-legitimate user. A second

approach to analysing password typing data. A method of collecting data from a web browser

by using JavaScript. Therefore, they determine four characteristics: the interval between key

pressure events, the interval between two key releases, and the interval between one key press

and release, also the opposite. The dataset comes from a 2009 study on keystroke dynamics

(Mhenni et al., 2018).

For veriﬁcation they used classiﬁcation methods by using K-nearest neighbours (KNN). It

provides high accuracy when it comes to keystroke dynamics. They used diﬀerent distance

metrics to increase the performance and accuracy. One was stastical distance another one





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

17

was hamming distance (Mhenni et al., 2018).

Xn

1

~~| − |~~

q

p

i

i

DSTAT = 1 −

e−

(2.4)

(2.5)

n

σ

i

i=1

DHAMMING = (#(qj = g (k))/n)

j

̸

In order to calculate 2.4 statistical distance metrics, biometric features are individually

analysed for statistical data. For competitive performances, the distance calculation is

commonly used. Predictions are generated based on the calculation speed. In 2.5 Hamming,

the percent diﬀerence between the labels and the novel query is calculated (Mhenni et al.,

2018).

Figure 2.11: Keystroke Authentication Process





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

18

(2.6)

(2.7)

v

u

Xm

u

t

2

DEUCLIDEAN

\=

(q − g (k))

i

j

k=1

Xm

DMANHATTAN

\=

|(q − g (k))|

i

j

k=1

To calculate the distance metrics in KNN, 2.6 Euclidean and 2.7 Manhattan distance calculation

methods were also used. To calculate the distance metrics in KNN, Euclidean and Manhattan

th

distance calculation methods were also used. q is the query for a user and j, g (k) is the k

i

j

reference sample of the user. j and m are the numbers of samples in the reference and gj

and µ is the mean vector and sigma was the standard deviation vector of references. N is the

length of the user, where i ranges from 1 to n (Mhenni et al., 2018).

The user was asked to enter password type data during the enrollment phase. The user

data was processed as a sample. After the data was received, it was added to the queue.

The query limit was set to 10. References do not rely on more than 10 datasets. To make

fast communication between server and database. After validating the dataset it goes to the

adaptation part. To make a decision, a standard threshold was set. It was based on a double

threshold to standardize. The ﬁrst one made a decision to accept or reject the data and the

second one made a decision to update or not. Adaptation of the data update to the system

during use of the system (Mhenni et al., 2018).

µ

j

−

i+1

i

j

Tj = T − e σj

(2.8)

i

µ and σ represent each user’s mean and standard deviation. In adaptation I, T was the

j

j

j

threshold and the j was the user. A semi-supervised learning approach is applied in these

modes. The labels were assigned by KNN classiﬁers. Diﬀerent distance matrixes were used

to get an optimal distance. Using each query to update the dataset, the whole dataset

works online. In addition, they proposed a double-serial mechanism for their experiments.

It waits until each data set has a length of 10, then switches to the old dataset to check the

experience. This works properly without any modiﬁcation as a self-learning process. In the

case of a veriﬁed decision, a consequence follows. Real-time updates are made to the reference

and threshold. With the help of the double serial mechanism they developed a stable model

of keystroke dynamics for users. A method of intra-class veriﬁcation was used (Mhenni et al.,

2018).

This study used two sets of data for validation: GREYC 2009 and WebGREYC. The dataset

was generated through the participation of 133 users. They are looking for 100 users for ﬁve

acquisition sessions over two months and 60 samples per user. In the webGREYC dataset 118

users participated but 45 of them only participated for 60 patterns data collection process.

For both the datasets, they consider 60 users each (Mhenni et al., 2018).





CHAPTER 2. LITERATURE SURVEY AND BACKGROUND

19

The stream generation method is used to extract the data from the user. The 60 samples

collected from users were entered into an evaluation protocol. They divided the process into

two parts. Each process had eight queries to the system. The data consists of ﬁve genuine

user records and three imposter records. A sample of ten genuine users was collected in a

batch as part of the study to collect a true user sample. In the database, the original user

data is arranged in sequential order. In this case, the imposter query runs at random. As a

result of that they obtain 12 sessions of adaptation where it calculates at 60/5. They divided

the dataset into two parts where the original user data was taken 37.5% which was calculated

from 3 by 8 and for the imposter they took 62.5% data. They calculated the data from 5 by

\8. The attack rates were higher than general keystroke attacks with 70% genuine and 30%

imposter data. They set the EER rate to 3%. They used 4 distance matrices to calculate the

result (Mhenni et al., 2018).

Referrene Size

Adaptive Mechanism Minimum Mazimum

Classiﬁer

KNN(Hamming)

KNN(Statistical)

KNN(Eculidean)

KNN(Manhattan)

SVM

EER

6.1%

AUC

0.013

0.017

0.033

0.031

\-

Double

Serial

1

1

1

1

5

5

5

10

10

10

10

15

15

15

6.3%

7.8%

8.9%

Avergae

Mechanism

[8]

6.96%

8.75%

10.75%

Neural Network

Statistical

\-

\-

Table 2.4: Classiﬁer Comparison with 2009 Databse

In Table 2.4, EER rate of 6.69% was the performance they received. When they used a SVM

classiﬁer, they compiled a sample of 5 samples of a minimum size and 15 samples of maximum

data. They used the same dataset from 2009 research. They got better results in EER and

Statistical distances. In static distance, the EER rate was 6.3%, and in hamming distance,

it was 6.1%. Oﬀer a facility for deploying the application to the server to take advantage

of low computing time. Their experiments refer to the evolution of size over a long period

of time. It is due to the fact that the number of set queries was not the same for all the

users. A rapid increase in the number of samples of data caused an interruption in the ﬂow

of data as a result. This is mainly due to the fact that sliding windows work better here

because of that. In addition, they found that the performance was being negatively aﬀected

by a slower growing window. Initially, the performance rate for the research was lower than

expected due to the weak recognition that was provided to new users at the beginning. This

refers to Manhattan distance in KNN. Other distances works really well specially Statistical

distance for the model. KNN struggle more than the other algorithms in terms of intra class

veriﬁcation since it has a smaller data size. The advantages of the algorithm are also used

for other algorithms in this literature. They tested the result for single data then checked for

multiple data (Mhenni et al., 2018).





Chapter 3

Implementation and Analysis

In this section of the report, the implementation and analysis will be discussed in extensive

detail. In the literature review, the previous work has been discussed in detail. In this study,

it was signiﬁcant to collect data from diﬀerent categories of people, and a total of 10-15

user data were collected. Previously, a public dataset was available from 2009 on password

typing veriﬁcation, and the application in these projects was implemented to authenticate

users based on their writing pattern. Therefore, the previous dataset could not be used for

implementation or training purposes.

3.1 Design

This project has been implemented using a number of libraries and languages. HTML,

Bootstrap CSS, and JavaScript are the components used to build the front end. As the key

to managing the layers of the application, the Flask framework has been used to develop

the application. Several challenges were faced during the implementation of the project. All

the web pages have been created in HTML and navigation are managed by ﬂask. A key

requirement of the project is the ability to determine whether the user is a legitimate user

or not. In order to achieve this, a database was required, and MongoDB was selected as

the online database server. In order to make it more dynamic and accessible to anyone with

a keyboard of any size. Additionally, it is capable of updating the database on a dynamic

basis. For the project to be successful, it has been necessary to engage in an interactive

session in order to experiment and achieve the desired results. In order to maintain secure

sessions between client and server, maintaining secure transactions has been of paramount

importance. Flask has that option to maintain the session securely with security key and

session key. Javascript was used as the ﬁrst target for collecting user data from web pages

and standardizing it into JSON format. After sending the message to the server, the server

should check the status of the user and return a response.

20





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

21

3.1.1 Front-end

It is developed using HTML, CSS, and JavaScript for the front end of the application. There

is a registration form Fig. 3.1 for the user to ﬁll out. The user can register using their

actual data or he or she can register anonymously using fake name and email id. In the

case of email, they can use fake addresses such as ”abc@mail.com”, ”123@mail.com”. At

present, the system does not validate email addresses because the actual user is not required

for testing. Furthermore, storing their personal details without their consent is unethical.

There is also an option for checking the email address to make sure there are no duplicates.

A login page Fig. 3.2 has also been created for a secure login system. Here, users can log in

Figure 3.1: Registration Page

using their email address and password that they used when registering with the system. A

new session is started for the speciﬁc user when the system conﬁrms that the email address

and password are identical.

Figure 3.2: Login Page

The Fig.3.3 homepage is created for the user to write on and the user name will appear at

the top of the page as the name they registered with. Those wishing to manually end their

session can do so by clicking the logout button.





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

22

Figure 3.3: Home Page

A Fig.3.4 logout page is also created if a user ends the session manually or their system

detects an unauthorized user.

Figure 3.4: Logout Page

3.1.2 Back-end

Flask

Compact frameworks, such as Flask, are micro-frameworks. Small enough to become easily

understandable and easy to learn from source code. It is important to note that size doesn’t

matter when it comes to functionality compared to other frameworks (Grinberg, 2018).

Flask app created for this application. It is necessary to generate a single secret key in

order to maintain a dynamic session key. Similarly, if the secret key is also set to dynamic

in every window slide, the browser will generate a new secret key and can’t compare or

remember the previous key, resulting in the session being cleared. Because the session is an

important key in this research, it won’t be a solution.

Figure 3.5: Secret Key





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

23

Figure 3.6: Session Key

A text encryption key is set in Fig. 3.5. In Flask, the key is stored in the back-end and

is used to generate the session based on that key. As shown in Fig. 3.6, a shared key is

generated following an elliptic curve diﬃe-hellman key exchange. In view of the fact that the

ﬂask handles the entire architecture, it is suﬃcient to use the shared key generated by the

server for the session key. An environment in which a server private key and a private key

are generated dynamically. The shard key is then derived from both the keys generated here.

The curves are smaller than 224 bits, but they are faster because they are based on NIST p

curves. As a result, the risk of a security breach is also reduced. According to safeCurves,

NIST is the only cryptography standard supported by the software. An elliptic curve follows

equation 3.1. P-256 is an elliptic curve that follows equation 3.2. Here, q represents the

underlying ﬁeld, and a, b represents the elliptic curve parameter, which in the case of P256

is 3. In a curve, point G is called the base point and point n is its base point (Adalier and

Teknik, 2015).

2

y = x + ax + b mod q

3

(3.1)

2

y = x + 3x + b mod q

3

(3.2)

A user ﬁlls out a form, submits it, and data is received in the Fig. 3.7 ”user registration”

function after it has been submitted using a POST method. Data is received and passed to

each variable separately. Combine name variables for storing into the database and in session.

To avoid redundancies, the email is checked before submission. The password is encrypted

using the bcrypt hashing algorithm.





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

24

Figure 3.7: Registration Back-end

A separate Fig. 3.8 login security function is developed. When the user submits his or

her email and password, the data will be sent to the security function. To begin with, it

checks whether the email type sent by the user is valid or not to prevent phishing attacks.

It will then determine whether the user is available and if so, it will obtain the users current

password. After that, encrypt the given password and compare it with the registered password

if they match. A session will be created and the session key will be set to the application if

every authentication is successful. In addition, the user’s full name and id will be stored in

the session cookie.





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

25

Figure 3.8: Secuirty Function

Authentication is performed with this last Fig. 3.9 function. An AJAX setup was used

in the front end to provide the data here. The JavaScript functions assist in the collection

of the data and its transmission to Flask via AJAX. In order to merge the user id with the

data, the function collects the user id from the session as soon as it receives the data. As

a starting point, a row is stored every 10 seconds for three minutes based on the current

behavior of that particular session and sent the data to the database. Afterwards, the data

will be gathered in the same manner, but rather than sending it to the database, it will be

stacked in a queue. It will be sent to a machine learning model for determining the status of

the user, and in return a response will be received. Depending on the response, the system

either stores the data in the database or clears the session by responding back to AJAX.





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

26

Figure 3.9: Authentication Function

Database

An example of a NoSQL database is MongoDB. For Craiglist use MongoDB is very popular in

the market. A document can easily be stored in MongoDB rather than a relational database

management system. The scalability and reliability is very high in MongoDB. A NoSQL

database is a diﬀerent kind of database from a relational database. Data no longer needs

to be ﬁxed based on the table like in a relational database. MongoDB follows JSON data

storage architecture where it creates documents with dynamic storage. It is called BSON.

MongoDB already has signiﬁcant capabilities and versatility for multiple languages (Boicea





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

27

et al., 2012). The purpose of this system is to store keystroke data with 20 diﬀerent features

of data within the keystroke dynamics collection. There are two types of user directories: the

user directory that maintains the login system, and the session that records the login time

at the time of every login.

Data Collect

Previous research has provided some key insights into the data collection process. For the

purpose of recognizing the pattern, ﬁve major key techniques were used. One is the Fig.

3.10 Key Hold process, which is the period of time between pressing a key and releasing it.

A second calculation is to determine the time interval between two keys being released. In

other words, it’s like when a user presses a key and then presses another without releasing

the ﬁrst. There is a process called Fig. 3.10 key down down. A third process is the opposite

of a down-down process. As a result of the user releasing two keys, the time between those

two events is called the Fig. 3.10 key up up period. Lastly, there is the Fig. 3.10 key up

down and the Fig. 3.10 key down up. An additional key press and release is calculated in

the same manner as a key release and a key press and release.

Figure 3.10: Key Example

There are a number of values coming from this pattern, and they are all calculated along

with their minimum value, maximum value, 3.3 average, and 3.4 standard deviation. To get

a better result.

Xn

1

A =

ai

(3.3)

N

i=1

σ = s

(3.4)

P

(x − µ)2

i

N





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

28

Figure 3.11: Keystroke Collection Process

The Table 3.1 data sample shows the values that were collected from diﬀerent users. The

points where diﬀerent user values diﬀer from each other for the same ﬁelds can be an excellent

learning method for machine learning. In the analysis of the data, it is found that the

maximum hold time detected by a user is 152 and the lowest is 124. A user has an 18.56

standard deviation and a maximum hold time of 144, but many other users have lower

maximums although their standard deviation value is higher than the user.. The standard

deviation is not aﬀected by the hold maximum. Each ﬁeld of data depends on the total time

period over which the data was generated.As a result of the max value instead of the hold

value, this feature has a higher value than the others. Among the lowest values in the table,

5 and 9 both represent up-down minimum values. This illustration shows the speed at which

a particular type of typer moves up and down. From this data, one can determine the speed

of the user. The maximum value for up down is too diﬀerent from most other users, where

one user has a value close to 1000 while another user has a value of 3592.





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

29





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

30

Figure 3.12: Feature Extraction

Figure 3.13: Feature Extraction





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

31

JavaScript is used to get features from HTML text boxes. Whenever a key is held, the current

timestamp is selected, stored with the key id in an object, and when the key is released, the

object value timestamp is deducted from the value with the current timestamp to calculate

the duration. All other methods require setup of two arrays for down and up. If someone

presses a key on the same key down function, check to see if the array length is greater than

0, then subtract that value from the current timestamp to calculate the down down time. By

subtracting that same timestamp from the last up time registered in the array, one will ﬁnd

the result of up down. It has been implemented in the same manner for the release of keys.

By subtracting the current timestamp from the last key up value, one can obtain the up up

time, and by subtracting last to last key down, one can obtain the time diﬀerence between

down and up.

Figure 3.14: Data Flow Diagram





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

32

The Fig. 3.14 illustrates. Throughout the process of authentication, a small amount of

data will be collected and sent to the validate model every three minutes at a time interval

of ten seconds as part of the authentication component. Additionally, a set of data will be

fetched every time an authentication request is sent to the server so that it can be processed.

There will be two sets of data, one of which will verify the authenticity of user data, and

another one of which will retrieve all the user data available in the database except the

actual user data. The prepossessing part will clean the data and convert that data into data

frame. It is easy to understand the normalization process, in which the values are normalized

to a single place.Separated the labels from the dataset as well. After normalization data

needs to prepare for the learning. So, the data split into two parts for both the databases.

Testing was conducted with a number of 50 users due to the minimum user participation

requirement, but the logic was designed to calculate the length of the actual user data as

compared to the imposter data. The length of the actual user data will determine the length

of the imposter data. Then, 50 percent of the data was used for training the model and the

remainder was used for testing. In the application, it will be 100% of the data since the

testing data or validation data will be derived from the actual session data. The labels of

imposter datasets will be changed to imposter instead of user id. Clusters will be created

after splitting. Prediction model and distance calculation are based on K-Nearest Neighbors.

A cluster size of 5 has been set. A model validation is a procedure in which a set of data will

be sent for model validation, and then the model will be predicted using the received accuracy

and false positive accuracy information. A result that appears to be an authorized user will

be sent to the database, and if it does not appear to be an authorized user, a response will be

sent in return and the session will be cleared and a redirection to the logout page will occur.

Figure 3.15: Data Collect

In Fig.3.15 pandas were used to manage and structure the data. To stop overﬁtting or

underﬁtting, replace 0 with the median of each column in the data cleaning part.





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

33

Figure 3.16: Normalization

In Fig. 3.16 a ﬁrst set of features was extracted from the dataset and the data was normalized

using the equation 3.5 Z-Score method. Labels were taken from the actual dataset and

separated out.

x − µ

x′ =

(3.5)

σ





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

34

Figure 3.17: Training Model

In Fig.3.17 a scanalar is selected to ﬁt the data. The calculation setup used the actual

length of the data in order to avoid an unbalanced model from arising. After that, the actual

data is split into XTrain and YTrain, and the imposter data is split into impXTrain and

impYTrain. A random state has been chosen for a consistent result. Again scale the data for

error redundancy. Imposter data labels set into imposter. xTrain merges with impXTrain and

yTrain is merged with impYTrain. A cluster taken 5 for KNN. This stage involves training

the model and scaling the temporary data.





CHAPTER 3. IMPLEMENTATION AND ANALYSIS

35

Figure 3.18: Prediction Model

In Fig.3.4, the length of the temporary data will be calculated. One confusion matrix will be

generated based on the data sent for prediction. The accuracy of the result will be determined

based on the results. Also classiﬁcation will be generated and that will be converted into a

data frame. In this way, a false positive will be removed and put into a condition where it

will be detected as an imposter if the false positive support reaches 40%. The result will be

the same even if the accuracy comes to 60% according to the user.





Chapter 4

Results

The result section is based on the analysis generated from collected data. 8-10 users participated

in the data collection procedure. The results are obtained based on the analysis of the

prediction for individual users.

4.1 Performance Measure of KNN

User

f1-score Accuracy Correct Incorrect

User 1

User 2

User 3

User 4

User 5

75

80

93

89

87

60%

66%

86%

80%

76%

9

6

5

2

3

3

10

13

12

10

Table 4.1: Genuin User Data

As you can see in the Fig. 4.1, this is based on actual data used by the user for a machine

learning training prediction. As a result, using the example of user 1, user got an accuracy

of 60% with 9 correct predictions and 6 incorrect predictions. In the case of this particular

user, the f1 score achieved was 75. There have already been challenges associated with the

accuracy of the previous research. In addition to the data, there are a number of other factors

that can aﬀect it. It is possible that a user is wearing gloves while typing or may be injured

or may only be using one hand while typing. To achieve a higher level of accuracy, data is

necessary and user interaction will make the process of gathering true data more eﬃcient.

Earlier research has shown that to make a positive decision, a minimum of 100 keystrokes

are needed. In the event that user data is incorporated well into the system, then there

is a higher chance of accuracy coming into play. In similar fashion, users 4 and 5 received

accuracy rates of 80% and 76%, respectively. A higher F1-score of 89 and 87 was received.

36





CHAPTER 4. RESULTS

37

User

f1-score Accuracy Correct Incorrect

User 1

User 2

User 3

User 4

User 5

33

43

83

93

95

80%

72%

28%

22%

10%

40

36

14

44

40

10

14

36

6

4

Table 4.2: Imposter Data

Fig. 4.2 shows the imposter data. The calculated in a diﬀerent way because the labels were

using genuine user labels that contained imposter data. Besides the logged in user, the rest

of the users in the database behave as if they were imposters. If the system trained well with

imposter data then the prediction will be most of the time imposter because they learned

most of the features of imposter. The system should learn about users more correctly with

imposter. The patterns are the key feature for the machine learning model. Here, user 1

and 2 received a good accuracy of 80% and 72%. The users data trained well to distinguish.

As for the rest of the users, they were not well trained and were mostly detected as genuine

users of the website.

4.1.1 Keystroke Patterns

The Fig. 4.1 shows the data length refers to the length of the keystroke rows collected from

the user, and frequency is determined by normalizing the keystroke values. Each pattern

diﬀers from the other. In spite of the fact that some patterns look similar, their ﬂuctuation

is diﬀerent. As a result of using equation 4.1 MinMax normalization, the data have been

normalized. A row of data is gathered from the user and the data varies from one row to

another based on the type of data collected. In some cases, graphs show stable patterns that

depict a stable writing pace and a steady writing pattern. If the user is unfamiliar with the

keyboard or has diﬃculty ﬁnding the keys while typing, the data might diﬀer depending on

whether the user is a regular user of the keyboard. Although some graphs look similar to

each other, they are entirely diﬀerent from each other in terms of their content and shape.

There is a huge diﬀerence between their starting point and their endpoint, as well as a vast

diﬀerence between their ﬂuctuation.

x − min(x)

i

zi =

(4.1)

max(x) − min(x)





CHAPTER 4. RESULTS

38

Figure 4.1: Keystroke Patterns of two user

4.1.2 Confusion Matrix

It is shown in the confusion matrix whether there are true positives or false positives. As

shown in the ﬁgure, it was initially detected as true 12 times and was originally a true label

for genuine users. 3 times it was detected as an imposter but it was a genuine user. It is

possible to improve the accuracy of the model by learning more about the user.





CHAPTER 4. RESULTS

39

Figure 4.2: Genuine Matrix

There are two diﬀerent labels available in the confusion matrix: user id and imposter, where

in the case of false data the genuine label has been merged. It is illustrated in the Fig. ??

that 15 times the user was detected as a genuine user, whereas 35 times the user was detected

as an imposter. This is a case in which the data is actually an imposter, so the prediction is

an imposter as well. If imposter varieties are available and stored in the database, or if the

imposter data is increased, the true positive of the model can be reduced in this section.

Figure 4.3: Imposter Matrix





CHAPTER 4. RESULTS

40

A data structure has been built using the JSON format for collecting and storing data.

As soon as the data is veriﬁed, it is sent to the database after authentication has been

successful.As shown in the Fig. 4.4.

Figure 4.4: JSON Data Structure

As shown in Fig. 4.5, there is a text box where the user can write, while the data is being

gathered in the background. Upon submitting a request, a response will be provided. It is

expected that the response will continue if the stack is collecting. A successful authentication

will be determined by the response to the authentication request. Otherwise, the system will

send an imposter and reroute the session to the logout page.





CHAPTER 4. RESULTS

41

Figure 4.5: Authentication Writing UI





Chapter 5

Conclusions and Future Work

A number of research studies have been conducted in the past. Occasionally, the target was

to analyse the user’s behaviour or to verify whether the user was genuine without identifying

the user or checking any additional veriﬁcation. The initial stage of the training includes

learning about keystrokes, as mentioned in Chapter 2. In order to verify a user, they stated

that at least 100 keystrokes are required. A study was conducted on the patterns of password

typing. Afterward, a research was conducted in 2009, and a dataset was generated based on

the results of this research. In this study, more than 100 individuals participated, and the

research took place over a period of two months.

As compared to previous research, the system is able to detect a person within 3 minutes

with only 18 keystrokes, which is much faster than previous research methods. I think that

the application can be improved if a greater number of people are able to participate in it.

It is very important that a balance is maintained between genuine people and those who are

imposters while learning. In the process of collecting data, there were several challenges that

had to be overcome. Typing at a higher speed and collecting data at a higher speed will

generate errors and large values. In addition, this aﬀects the training model and makes it

diﬃcult to normalise the data in a meaningful way. A semi supervised learning approach is

used to develop it. This model works as supervised learning, but the data changes on every

run if the user is genuine. A reinforcement learning model can be developed after collecting

eﬀective data from users or an API can be developed so that any web application can use it.

The number of data required to make a professional application for companies depends on

the type of user and the type of information they provide. There can be professional typist,

occasional users of the keyboard, or people who type on a daily basis, but not a professional

typist. Additionally, diﬀerent types of keyboards have to be collected along with the data in

a number of diﬀerent scenarios. As soon as the research is completed, the data can be useful

for authentication. It will take a long time to implement and fund the research. Researchers

have already developed some applications for smartphones that have not been implemented

in real life. Future web and mobile applications will be able to combine keystroke dynamics,

42





CHAPTER 5. CONCLUSIONS AND FUTURE WORK

43

mouse dynamics, and touch sensitivity. There is a major challenge to implement to ensure

that companies do not monitor their activities such as storing what they type and what they

do in their daily activities. A major security concern for users can result from this situation.

If this is implemented and companies begin storing user patterns, security measures must be

taken to prevent replication in the future.

A variety of applications can be developed based on the keystroke dynamics. However,

mouse dynamics must also be integrated with keystrokes for it to be eﬀective for social media

websites. It is important to consider mouse dynamics such as the x and y axis, button

action, button type, and mouse speed. The system may also be implemented by companies

in order to secure the internal system used by their employees. It is possible to prevent third

parties from accessing the system. Detecting shell script users can also be solved with this

technique. Hackers can be prevented from making use of it, and automated attacks can also

be prevented. In order to accomplish that, the application must have full control over the

DOM or it must be integrated with the operating system. Furthermore, if the model is not

trained, then this can also pose a problem.





Bibliography

Adalier, M. and Teknik, A. (2015). Eﬃcient and secure elliptic curve cryptography

implementation of curve p-256. In Workshop on elliptic curve cryptography standards,

volume 66, pages 2014–2017.

Boicea, A., Radulescu, F., and Agapin, L. I. (2012). Mongodb vs oracle–database comparison.

In 2012 third international conference on emerging intelligent data and web technologies,

pages 330–335. IEEE.

Contributors, W. (2019).

Authentication.

[online] Wikipedia. Available at:

https://en.wikipedia.org/wiki/Authentication [Accessed Jun. 24AD].

Crockford, D. (2008). JavaScript: The Good Parts: The Good Parts. ” O’Reilly Media, Inc.”.

Downey, A. (2012). Think python. ” O’Reilly Media, Inc.”.

G´eron, A. (2017). Hands-on machine learning with scikit-learn and tensorﬂow: Concepts.

Tools, and Techniques to build intelligent systems.

Grinberg, M. (2018). Flask web development: developing web applications with python. ”

O’Reilly Media, Inc.”.

Hastie, T., Tibshirani, R., Friedman, J. H., and Friedman, J. H. (2009). The elements of

statistical learning: data mining, inference, and prediction, volume 2. Springer.

inwedo (2022). What is token-based authentication?

[online] inwebo. Available at:

https://www.inwebo.com/en/authentication-token/ [Accessed Jul. 27AD].

Javatpoint (2021). (examples of ai (artiﬁcial intelligence) - javatpoint, 2022). [online]

Available at:https://www.javatpoint.com/examples-of-ai [Accessed Aug. 30AD].

Jos´e, I. (2018).

(knn (k-nearest neighbors) 1).

[online] Medium. Available

at: https://towardsdatascience.com/knn-k-nearest-neighbors-1-a4707b24bd1d [Accessed 9

Sep. 2022].

kaggle

(2020).

(100,000

uk

used

car

data

set).

[online]

https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes

[Accessed 9 Sep. 2022].

44





BIBLIOGRAPHY

45

Killourhy, K. S. and Maxion, R. A. (2009). Comparing anomaly-detection algorithms for

keystroke dynamics. In 2009 IEEE/IFIP International Conference on Dependable Systems

& Networks, pages 125–134. IEEE.

Meyer, E. A. (2006). CSS: The Deﬁnitive Guide: The Deﬁnitive Guide. ” O’Reilly Media,

Inc.”.

Mhenni, A., Cherrier, E., Rosenberger, C., and Amara, N. E. B. (2018). Towards a secured

authentication based on an online double serial adaptive mechanism of users’ keystroke

dynamics. In International Conference on Digital Society and eGovernments (ICDS).

N-Able (2019). Understanding network authentication methods. [onlin+e] N-able. Available

at: https://www.n-able.com/blog/network-authentication-methods [Accessed Jun. 24AD].

Nixon, R. (2014). Learning PHP, MySQL & JavaScript: With jQuery, CSS & HTML5. ”

O’Reilly Media, Inc.”.

okta (2021). Authentication token: what is it? how does it work? [online] Available at:

https://www.okta.com/uk/identity-101/what-is-token-based-authentication/

Jul. 28AD].

[Accessed

Python, W. (2021). Python. Python Releases for Windows, 24.

Raggett, D., Le Hors, A., Jacobs, I., et al. (1999). Html 4.01 speciﬁcation. W3C

recommendation, 24.

Shepherd, S. (1995).

Continuous authentication by analysis of keyboard typing

characteristics. In European Convention on Security and Detection, 1995., pages 111–114.

IET.

Siddiqui, N., Pryor, L., and Dave, R. (2021). User authentication schemes using machine

learning methods—a review. In Proceedings of International Conference on Communication

and Computational Technologies, pages 703–723. Springer.

Vallat, R. (2018). Pingouin: statistics in python. J. Open Source Softw., 3(31):1026.

Van Rossum, G. and Drake Jr, F. L. (1995). Python tutorial, volume 620. Centrum voor

Wiskunde en Informatica Amsterdam, The Netherlands.


=======
# Dissertation
1. The app develoed in flask. 
2. Conda enviornment is requierd to run the app locally.
3. All Liabaries need to install to the anaconda envionment.
4. Data is storing in online MongoDB storage.

Deployed to heroku. Code uploded to github account and connect with heroku.

Online Link: https://continues-auth.herokuapp.com/
Footer
© 2022 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
>>>>>>> 9526d0a5b72600fa4fab1903c3c3f1dcf356eeaf
