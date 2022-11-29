from pygame import mixer

class Music: 
	def __init__(self):
		#initializes mixer 
		mixer.init()
		self.song1 = mixer.music.load('swedenSnippet.mp3')
		self.song2 = mixer.mucis.load('Upbeat_Tutorial.mp3')
		mixer.music.set_volume(0.2)
		mixer.music.play()

