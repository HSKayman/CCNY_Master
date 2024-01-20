TRAINING A CNN FOR SPEECH RECOGNITION

In this assignment, you will create a CNN to recognize spoken phrases from one
language and translate them to another language(s).

At the beginning, you will create several sub-directories inside 
ReferenceSet and TrainingSet directories:
    (a) In ReferenceSet directory:
        - Create a new directory for each output language
          that the CNN is able to translate to. For example,
          if the CNN translates words from Korean to both
          German and Russian, create the directories "German"
          and "Russian" inside ReferenceSet.
	  - Inside each of the language directories, create a new subdirectory 
	    for each phrase to be recognized; typically the subdirectory is named 
	    to represent the phrase (e.g., a subdirectory called "you_are_welcome" 
	    is suitable for storing reference audio for the phrase 
	    "you are welcome").
	    Note that the names of the subdirectories must match across each 
	    language directory.
	    Also note that there should be only one file per phrase in each of 
	    the language directories.
    (b) In TrainingSet directory:
        - Create a new directory for each phrase to be recognized. 
	  Note that the names of the directories in TrainingSet must match to
	  phrase subdirectories in each of the ReferenceSet language directories.

Below is an example of how the directory tree should look like for 
a CNN that can translate the phrases "hello", "thank you", and "good bye"
from Chinese to Russian or Spanish:

            ReferenceSet
            |
            |---Russian
            |   |
            |   |---hello
            |   |
            |   |---thank_you
            |   |
            |   |---good_bye
            |
            |---Spanish
            |   |
            |   |---hello
            |   |
            |   |---thank_you
            |   |
            |   |---good_bye


            TrainingSet
            |
            |---Chinese
                |
                |---hello
                |
                |---thank_you
                |
                |---good_bye
             

After the subdirectories are created, they should be populated by
running Matlab program called create_new_audio.m:

create_new_audio.m: (This file is not to be modified by the students)
    (a) This program records phrases to be used both
        as reference audio and CNN training audio;
    (b) The user is asked to say a phrase into the microphone;
    (c) Recording audio to be used as reference:
		(1) The user is prompted to enter the language of 
		    the phrase (e.g., "German"). 
		(2) The user is then prompted to name the phrase itself 
		    (e.g.  "you_are_welcome"). 
		(3) The user is then asked to give a filename for the 
		    recorded audio (e.g., "you_are_welcome_german_ref"). 
		(4) Based on the information provided by the user, the 
		    recorded phrase is then saved inside ReferenceSet 
		    under the appropriate sub-directory.
        
		 (For example, under "ReferenceSet/German/you_are_welcome"
		 directory, there will be a single audio file in German 
		 for the phrase "you are welcome" saved as a file called
		 "you_are_welcome_german_ref.wav")

    (d) Recording audio to be used as training sample for by CNN:
		(1) The user is prompted to enter the language of 
		    the phrase (e.g., "Korean"). 
		(2) The user is then prompted to name the phrase itself 
		    (e.g.  "you_are_welcome"). 
		(3) The user is then asked to give a filename for the 
		    recorded audio (e.g., "you_are_welcome_korean_3"). 
		    Note that there will be multiple training files for the
		    same phrase in the same directory. You should uniquely
		    name each file.
		(4) Based on the information provided by the user, the 
		    recorded phrase is then saved inside TrainingSet 
		    under the appropriate sub-directory.

	         (For example, under "TrainingSet/your_welcome" directory 
		 may contain many Korean recordings of the phrase 
		 "you are welcome" saved as "your_welcome_korean_1.wav", 
		 "your_welcome_korean_2.wav", etc.)

Below is an example of how the directory tree should look like for 
a CNN that can translate the phrases "hello", "thank you", and "good bye"
from Chinese to Spanish after populating it with audio files:

            ReferenceSet
            |
            |---Spanish
                |
                |---hello
                |   |---hello_spanish_ref.wav
                |
                |---thank_you
                |   |---thank_you_spanish_ref.wav
                |
                |---good_bye
                    |---good_bye_spanish_ref.wav

            TrainingSet
            |
            |---Spanish
                |
                |---hello
                |   |---hello_spanish_train_1.wav
                |   |---hello_spanish_train_2.wav
                |   |---hello_spanish_train_3.wav
                |
                |---thank_you
                |   |---thank_you_spanish_train_1.wav
                |   |---thank_you_spanish_train_2.wav
                |
                |---good_bye
                    |---good_bye_spanish_train_1.wav
                    |---good_bye_spanish_train_1.wav
                    |---good_bye_spanish_train_1.wav
                    |---good_bye_spanish_train_1.wav


After the TrainingSet and ReferenceSet directories are populated with 
audio files, now the CNN can be defined and trained as follows:

pro_9_speech_x.m: (This is the main program that runs the project. Do not
                modify anything in this file except for the function called
                cnn_train())
	(a) This is the main program that runs CNN for the project.
	(b) This program prompts the user to either create a new CNN or load an
	    existing one:
		(1.a) If the user chooses to train a new CNN, it calls cnn_train().
		(1.b) If the user chooses to use a previously trained CNN, it loads 
		      a CNN existing in the same directory saved previously as
		      a .mat file.
	(c) It then calls cnn_predict(), which asks the user to say a phrase.
	(d) Then cnn_predict() passes the recorded phrase to the trained CNN, 
	    which recognizes the phrase and plays it back in the selected language.

cnn_train(): (This function is located at the bottom of pro_9_speech_x.m. It is
              given as a skeleton to be modified by the students)
    (a) This function defines the architecture of CNN as follows:
        - CONV LAYER (size, number of filters)
        - BATCH NORMALIZATION
        - RELU
        - POOL(size, stride)
        - CONV LAYER (size, number of filters)
        - BATCH NORMALIZATION
        - RELU
        - POOL(size, stride)
        - CONV LAYER (size, number of filters)
        - BATCH NORMALIZATION
        - RELU
        - FULLY CONNECTED ANN
    (b) Once these layers are defined, it then trains the CNN using the audio data
	saved in TrainingSet directory.

