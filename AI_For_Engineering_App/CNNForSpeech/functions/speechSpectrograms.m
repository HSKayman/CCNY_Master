% speechSpectrograms(ads,segmentDuration,frameDuration,hopDuration,numBands)
% computes speech spectrograms for the files in the datastore ads.
% segmentDuration is the total duration of the speech clips (in seconds),
% frameDuration the duration of each spectrogram frame, hopDuration the
% time shift between each spectrogram frame, and numBands the number of
% frequency bands.
function X = speechSpectrograms(ads,segmentDuration,frameDuration,...
    hopDuration,numBands,fs)

disp("Computing speech spectrograms...");

%fs        = 16e3;
FFTLength = 512;
persistent filterBank
if isempty(filterBank)
   filterBank = designAuditoryFilterBank(fs,'FrequencyScale','mel',...
                                            'FFTLength',FFTLength,...
                                            'NumBands',numBands,...
                                            'FrequencyRange',[50,7000]);
end
numHops = ceil((segmentDuration - frameDuration)/hopDuration);
numFiles = length(ads.Files);
X = zeros([numBands,numHops,1,numFiles],'single');
for i = 1:numFiles
    
    x = read(ads);
    
    frameLength = round(frameDuration*fs);
    hopLength = round(hopDuration*fs);
    
    [~,~,~,spec] = spectrogram(x,hann(frameLength,'periodic'),...
        frameLength - hopLength,FFTLength,'onesided');
    spec = filterBank * spec;

    % If the spectrogram is less wide than numHops, then put spectrogram in
    % the middle of X.
    w = size(spec,2);
    left = floor((numHops-w)/2)+1;
    ind = left:left+w-1;
    X(:,ind,1,i) = spec;
    
    if mod(i,1000) == 0
        disp("Processed " + i + " files out of " + numFiles)
    end  
end
disp("...done");
end