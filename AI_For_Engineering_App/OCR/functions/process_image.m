function img_mat = process_image(ax)
    target_size = 28;
    
    % convert image to a grayscale image
    F = getframe(ax);
    [X, ~] = frame2im(F);
    for i = 1:size(X,1)
        for j = 1:size(X,2)
            if(X(i,j,1) == X(i,j,2)  &&  X(i,j,1) == X(i,j,2))
               X(i,j,1) = 255;
               X(i,j,2) = 255;
               X(i,j,3) = 255;
            end
        end
    end

    grayX = double(rgb2gray(X));

    % normalize the grayscale image
    grayX = grayX - min(min(grayX));
    grayX = grayX / max(max(grayX));
    grayX = uint8(grayX*255);

    grayX = thicken_lines(grayX,5);
    
    % process the image
    img_mat = grayX;
    [height,~] = size(img_mat);

    % crop excess extra space
    while(sum(img_mat(:,1)) == (255 * height))
        img_mat = img_mat(:,2:end);
    end

    while(sum(img_mat(:,end)) == 255 * height)
        img_mat = img_mat(:,1:end-1);
    end

    [~,width] = size(img_mat);

    while(sum(img_mat(1,:)) == 255 * width)
        img_mat = img_mat(2:end,:);
    end
    
    while(sum(img_mat(end,:)) == 255 * width)
        img_mat = img_mat(1:end-1,:);
    end

    % make the image square
    dim = size(img_mat);
    difference = abs(dim(1)-dim(2));

    if(dim(1) < dim(2))
        img_mat = cat(1,zeros(ceil(difference/2),dim(2))+255,img_mat);
        img_mat = cat(1,img_mat,zeros(floor(difference/2),dim(2))+255);
    elseif(dim(2) < dim(1))
        img_mat = cat(2,zeros(dim(1),ceil(difference/2))+255,img_mat);
        img_mat = cat(2,img_mat,zeros(dim(1),floor(difference/2))+255);
    end

    % resize the image and add padding
    new_size = target_size - 2*ceil(target_size/10);
    img_mat = imresize(img_mat, [new_size new_size]);

    img_mat = img_mat - min(min(img_mat));
    img_mat = img_mat / max(max(img_mat));
    img_mat = uint8(img_mat*255);
    img_mat_mode = mode(mode(img_mat));
    
    for i = 1:size(img_mat,1)
        for j = 1:size(img_mat,2)
            if img_mat(i,j) == img_mat_mode
                img_mat(i,j) = 255;
            end
        end
    end
    
    difference = target_size - new_size;
    img_mat = cat(1,zeros(ceil(difference/2),new_size)+255,img_mat);
    img_mat = cat(1,img_mat,zeros(floor(difference/2),new_size)+255);

    img_mat = cat(2,zeros(target_size,ceil(difference/2))+255,img_mat);
    img_mat = cat(2,img_mat,zeros(target_size,floor(difference/2))+255);
    
end

function result = thicken_lines(X,line_width)
    result = zeros(size(X));
    result = result + 255;
    for i = 1:size(X,1)
        for j = 1:size(X,2)
            if is_near_line(X,line_width,i,j)
                result(i,j) = 0;
            else
            end
        end
    end
    % remove the line at the right hand side (fix a bug);
    for i = 1:size(result,1)
        for j = (size(result,2)- 10):size(result,2)
            result(i,j) = 255;
        end
    end
end

function result = is_near_line(X,line_width,row,col)
    for i = -line_width:line_width
        for j = -line_width:line_width
            if (row+i < 1  ||  row+i > size(X,1))
                % do nothing
            elseif (col+j < 1  ||  col+j > size(X,2))
                % do nothing
            elseif X(row+i,col+j) ~= 255  &&  (i^2 + j^2) <= line_width^2
                result = 1;
                return
            else
                % do nothing
            end
        end
    end
    result = 0;
end