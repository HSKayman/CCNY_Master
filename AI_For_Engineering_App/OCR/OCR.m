
clc;
clear;
% select training directory
train_dir = 'TrainingSet'; 
% select reference directory
ref_dir = 'ReferenceSet';
%output directory
saved_cnns = 'Saved_CNNs';

if exist('functions','dir') == 7
    % get access to all files in the 'functions' directory
    addpath('functions');
else
    error("Error: Unable to locate 'functions' directory")
end

message = sprintf('WELCOME TO USING PHONE SECURITY CNN. MAKE YOUR SELECTION:');
disp(message);
disp('Enter 1 to train a new CNN');
disp('Enter 2 to load an existing CNN');
user_entry = input('Enter your choice: ');
    
if (user_entry == 1)
    % train a new CNN:
    disp('Be patient until statistics are displayed...');
    cnn_trained = cnn_train(train_dir);
    input('CNN training is complete. Press enter to start using CNN.\n');
elseif (user_entry == 2)
    % use an existing CNN:
    cnn_file = input('Enter CNN name (dont forget .mat extension): ', 's');
    cnn_path = pwd;
    disp(cnn_file);
    try
        % load the CNN and assign it to cnn_trained
        load_data = load(fullfile(cnn_path, saved_cnns, cnn_file));
        cnn_trained = load_data.cnn_trained;
    catch
        disp('Enter a valid file name next time... Leaving... Bye');
        return;
    end
else
    disp('Enter a valid choice next time... Leaving... Bye');
    return;
end

% Now there is a trained CNN loaded (either a new one or an existing one).
% Use trained CNN to make predictions:

% start drawing a character using drawtool.m found in the 
% functions directory
image = draw_tool();

% CNN predicts the character
cnn_prediction = cnn_predict(cnn_trained, ref_dir, image);

user_entry = input('Do you want to save CNN? (y/n) ','s');
if(user_entry == 'y')
    file_name = input('Enter file name (do not forget .mat extension): ',...
        's');
    save(fullfile(saved_cnns,file_name), 'cnn_trained');
else   
end
disp('Have a predictably nice day!');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%% END OF PROGRAM %%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function Prediction = cnn_predict(net,ref_path,char_img)
% this GUI shows prediction for the character drawn by the user 

    S.net = net;
    S.ref = ref_path;
    % open a window(figure) for the GUI
    S.fh = figure('units','pixels',...
                'position',[500 300 600 400],...
                'menubar','none',...
                'name','Character Recognition Using CNN',...
                'numbertitle','off',...
                'resize','off',...
                'Color',[0.8588 0.9412 0.8275]);
        
    % create an axes to hold the images
    S.ax = axes('units','pix',...
               'position',[100 250 200 90]);
    % pass the drawing to the CNN and get a prediction
    [Prediction,~] = classify(net, char_img);
    
    % retreive the appropriate reference image for prediction
    full_ref_path = fullfile(ref_path,char(Prediction));
    ref_imd = imageDatastore(full_ref_path);
            
    % display user input image
    subplot(1,2,1);
    imshow(char_img);
    title('YOUR CHARACTER','FontSize',15);

    % display prediction image
    subplot(1,2,2);
    imshow(ref_imd.Files{1});
    title('CNN PREDICTION','FontSize',15);
end

%% MAKE MODIFICATIONS BELOW

function net = cnn_train(train_dir)
% Train a new CNN using images from TrainingSet directory
% Then return trained CNN

    %%%%%%%%%%% TRAIN THE CNN %%%%%%%%%%%
    
    % load the training image dataset into an imageDatastore
    
    imds_train = imageDatastore(train_dir, 'IncludeSubfolders', true, 'LabelSource', 'foldernames');
    
    % get the number of unique training labels in the training data:
    numClasses = numel(categories(imds_train.Labels));
                           
    layers = [
        % set the size of the input image as 28x28 pixels with 1 color 
        % channel (grayscale):
        imageInputLayer([28 28 1])
        
        % Add the following layers to the CNN:
        %     - CONV LAYER (size = 3x3, noof filters = 10)
        convolution2dLayer(3, 10, 'Padding', 'same')
        %     - BATCH NORMALIZATION
        batchNormalizationLayer
        %     - RELU
        reluLayer
        %     - POOL(size = 2x2, stride = 2)
        maxPooling2dLayer(2, 'Stride', 2)
        %     - CONV LAYER (size = 3x3, noof filters = 20)
        convolution2dLayer(3, 20, 'Padding', 'same')
        %     - BATCH NORMALIZATION
        batchNormalizationLayer
        %     - RELU
        reluLayer
        %     - POOL(size = 2x2, stride = 2)
        maxPooling2dLayer(2, 'Stride', 2)
        %     - CONV LAYER (size = 3x3, noof filters = 40)
        convolution2dLayer(3, 40, 'Padding', 'same')
        %     - BATCH NORMALIZATION
        batchNormalizationLayer
        %     - RELU
        reluLayer
        
        % create the ouput (ANN) layer by using a fully connected layer.
        % the number of neurons in the output layer is equal to the number
        % of image labels:
        fullyConnectedLayer(numClasses)
        
        % use a softmax layer to convert the outputs to a set of 
        % probabilities where each output represents the probability that the
        % image is a corresponding label:
        softmaxLayer
        
        % add a classification layer to make each output mutually
        % exclusive, in other words there's only a single correct label for 
        % each image:
        classificationLayer
        ];
    %END OF layers

    % specify CNN training options:
    options = trainingOptions('sgdm', ...
        'InitialLearnRate', 0.01, ...
        'MaxEpochs', 10, ...
        'Shuffle', 'every-epoch', ...
        'Verbose', true, ...
        'Plots', 'training-progress');
    
    % sleep for a second to display the GUI
    pause(1);
    
    % start training the CNN
    net = trainNetwork(imds_train, layers, options);
    
end

