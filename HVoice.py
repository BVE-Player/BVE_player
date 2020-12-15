import playsound
import speech_recognition as sr
from gtts import gTTS as tts


class H_Voice:

    def __init__( self ):
        self.listMsg = []
        self.strMsg = ""
        self.objRecognizer = sr.Recognizer()
        self.objMicroPhone = sr.Microphone()

    def getMsg( self ):
        strMsg = self.strMsg
        self.strMsg = ""
        return strMsg


    def listen_background( self ):
        self.stop_listen = self.objRecognizer.listen_in_background( self.objMicroPhone, self.callback )

    def stop_listen_background( self ):
        self.stop_listen( wait_for_stop=False )

    def callback( self, recognizer, audio ):
        try:
            strMsg = recognizer.recognize_google( audio, language='ko' )
            print( self.strMsg )
            self.strMsg = strMsg
        except Exception as e:
            print( "Exception: " + str( e ) )