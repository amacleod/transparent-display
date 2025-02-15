clear all
close all
clc


% Load image
pathName = 'C:\Users\Dennis\Desktop\Projects\Arduino\images';
fileName = 'Bourbeau_FESCenter.jpg';
% fileName = 'circle.png';
origImage = imread(fullfile(pathName,fileName));

% Convert image to monochrome
grayImage = rgb2gray(origImage);
% grayImage = origImage;
histogram(grayImage);
imThresh = 160;
bwImageLg = grayImage > imThresh;
% bwImageLg = grayImage <= imThresh;

% Rescale and resize image to 56x128 resolution
imScale = 128/size(grayImage,2);
bwImage = imresize(bwImageLg,imScale);
horzLine = 47;
bwImage = bwImage(horzLine-28:horzLine+27,:);

% Convert binary image matrix to hexadecimal matrix and write to file
% txtPath = 'C:\Users\Dennis\Documents\Arduino\CFAL12856A00151B\images';
txtPath = pathName;
txtFile = 'Dennis.txt';
% txtFile = 'circle.txt';
fileID = fopen(fullfile(txtPath,txtFile),'w');
fprintf(fileID,'  { \n');
hexIm = cell(1,size(bwImage,2));
for iiRow = 1:8:size(bwImage,1)
    fprintf(fileID,'    {');
    for iiCol = 1:size(bwImage,2)
        hexIm{1,iiCol} = ['0x' binaryVectorToHex(bwImage(iiRow:iiRow+7,iiCol)','LSBFirst')];
        if iiCol ~= size(bwImage,2)
            fprintf(fileID,[hexIm{1,iiCol} ',']);
        else
            fprintf(fileID,hexIm{1,iiCol});
        end
    end
    fprintf(fileID,'}, \n');
%     fprintf(fileID,formatSpec
end
fprintf(fileID,'  }; \n');
fclose(fileID);

% Show Image
% imshow(origImage)
% imshow(grayImage)
% imshow(bwImageLg)
imshow(bwImage)

