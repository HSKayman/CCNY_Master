function [] = PlayBack_Translation(recObj, ref_ads)
%PlayBack_Translation 
    % enable text to speech
    NET.addAssembly('System.Speech');
    obj = System.Speech.Synthesis.SpeechSynthesizer;
    % set volume of text to speech
    obj.Volume = 100;
    
    % text to speech
    Speak(obj, 'Your word');
    
    % playback the user's word
    play(recObj);
    recording_duration = recObj.TotalSamples / recObj.SampleRate;
    pause(recording_duration);
    
    % text to speech
    Speak(obj, 'Translation');
    
    % play the translated word from a reference file
    [y,Fs] = audioread(ref_ads.Files{1});
    sound(y,Fs);
end

