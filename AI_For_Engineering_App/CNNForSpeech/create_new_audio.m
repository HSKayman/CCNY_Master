clc;
clear;

% 1. good morning
% 2. thank you
% 3. how much?
% 4. too expensive
% 5. grocery store
% 6. airport
% 7. taxi stand
% 8. restaurant
% 9. bus stop
% 10. good bye

% select training directory
train_dir = 'TrainingSet'; 
% select reference directory
ref_dir = 'ReferenceSet';

disp('****************************************************');
disp('** WELCOME TO THE SPEECH RECOGNITION DATA CREATER **');
disp('****************************************************');

input('\nPress ENTER to start\n\n');

% setup recording parameters for microphone
sample_rate = 16000;
bits_per_sample = 8;
noof_channels = 1;
recording_duration = 2;

% create the object that performs recording:
recObj = audiorecorder(sample_rate, bits_per_sample, noof_channels);

finished = false;
while (~finished)
    input('PRESS ENTER AND IMMEDIATELY SAY A WORD INTO YOUR MICROPHONE');
    disp('Recording...');

    % recording now:
    recordblocking(recObj, recording_duration);

    % playback the voice recorded:
    disp('Replaying recording...');
    play(recObj);
    pause(recording_duration);
    
    choice = input('Do you want to save this recording? (y/n) \n','s');
    if (choice == 'y')
        fprintf('\nEnter 1 to save as training data');
        fprintf('\nEnter 2 to save as a reference\n');
        
        type = input('\nEnter your choice: ','s');
        
        if type == '1'
            directories = dir(train_dir);
        elseif type == '2'
            directories = dir(ref_dir);
        else
            disp('Enter a valid option next time... Leaving... Bye');
            return;
        end
        
        % read languages from reference directory and store them into 
        % a list
        languages = {};
        for i = 1:length(directories)
            directory = directories(i);
            if directory.isdir && ~strcmp(directory.name,'.')...
                    && ~strcmp(directory.name,'..')
                % append languages with directory.name
                languages{length(languages)+1} = directory.name;
                fprintf('Enter %d for %s\n', length(languages),...
                    directory.name);
            end
        end
        fprintf('Enter %d to add a new language\n',...
                length(languages) + 1);
        choice = input('\nSelect the language of the recording: ');
        if (choice == length(languages) + 1)
            language = input('\nType the new language to add: ','s');
            mkdir(fullfile(ref_dir, language));
        else
            language = languages{choice};
        end
        
        if type == '1'
            output_dir = fullfile(train_dir, language);
        elseif type == '2'
            output_dir = fullfile(ref_dir, language);
        end
        
        
        
%%%%%%%%%%%%%%%%%%%%        
        
        if length(dir(output_dir)) > 2
            ads = audioDatastore(output_dir, ...
                                   'IncludeSubfolders',true, ...
                                   'LabelSource','foldernames');
            % get a list of unique labels
            labels = categories(ads.Labels);
        else
            labels = [];
        end
        
        for i = 1:length(labels)
            fprintf('Enter %d for %s\n', i, labels{i});
        end
        fprintf('Enter %d to add a new phrase\n\n', length(labels)+1);
        
        choice = input('\nEnter your choice: ');
        
        if (choice == length(labels) + 1)
            label = input('\nType the new phrase to add: ','s');
            mkdir(fullfile(output_dir, label));
        else
            label = labels{choice};
        end
        
        output_dir = fullfile(output_dir, label);
        
        file_name = input('Enter a file name for the recording: ','s');
        
        y = getaudiodata(recObj);
        Fs = recObj.SampleRate;
        file_path = fullfile(output_dir,strcat(file_name,'.wav'));
        audiowrite(file_path,y,Fs);
        
        disp('Successfully saved recording as:');
        disp(file_path);
    end
    
    choice = input('Do you want to create another recording? (y/n)\n','s');
    if (choice ~= 'y')
        finished = true;
    end
end
disp('Have a nice day!');