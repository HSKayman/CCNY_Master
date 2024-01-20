% ORIGINAL SCRIPT WRITTEN BY: Alec Jacobson
% SOURCE: http://www.alecjacobson.com/weblog/?p=2473

function P = get_curve(f)
% get_curve(f): Get a curve (sequence of points) from the user by 
%               dragging on the current plot window
% 
% Inputs:
%   f  figure id
% Outputs:
%   P  #P by 2 list of point positions
%
    
    % Get the input figure or get current one (creates new one if none
    % exist)
    if nargin == 0 || isempty(f)
        f = gcf;
    end
    figure(f);
    
    draw_color = [0 0.447 0.741];

    % get axes of current figure (creates on if doesn't exist)
    a = gca;

    % freeze axis
    axis manual;
    % set view to XY plane
    view(2);

    %set(gcf,'windowbuttondownfcn',@ondown);
    set(gca,'ButtonDown',@ondown);
    set(gcf,'keypressfcn',@onkeypress);
    set(gcf,'DeleteFcn',@onDelete);
    % living variables
    P = [];
    p = [];

    % loop until mouse up, window is closed or ESC is pressed
    done = false;
    while(~done && ishandle(f))
        set(f,'defaultAxesColorOrder',draw_color)
        drawnow;
    end

    % Callback for mouse press
    function ondown(src,ev)
        % Tell window that we'll handle drag and up events
        set(gcf,'windowbuttonmotionfcn', @ondrag);
        set(gcf,'windowbuttonupfcn',     @onup);
        append_current_point();
    end

    % Callback for mouse drag
    function ondrag(src,ev)
        append_current_point();
    end

    % Callback for mouse release
    function onup(src,ev)
        % Tell window to handle down, drag and up events itself
        finish();
    end

    % Callback for closing the figure window
    function onDelete(src,ev)
        finish();
    end

    function onkeypress(src,ev)
        % escape character id
        ESC = char(27);
        switch ev.Character
        case ESC
            finish();
        otherwise
            error(['Unknown key: ' ev.Character]);
        end
    end

    function append_current_point()
        % get current mouse position
        cp = get(gca,'currentpoint');
        % append to running list
        P = [P;cp(1,:)];
        if isempty(p)
            % init plot
            hold on;
            p = plot(P(:,1),P(:,2));
            hold off;
        else
            % update plot
            set(p,'Xdata',P(:,1),'Ydata',P(:,2));
        end
    end

    function finish()
        done = true;
        set(gcf,'windowbuttonmotionfcn','');
        set(gcf,'windowbuttonupfcn','');
        set(gca,'ButtonDown','');
        set(gcf,'keypressfcn','');
        set(gcf,'DeleteFcn','');
    end

end