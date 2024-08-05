%% Program to plot csv files from cantilever experiment


% Path to the csv files folder
directorio = '/Users/damiangimeno/Desktop/Masters ME/Research/Cantilever/New boundary conditions, most sensitive cantilever/valley green/data for video, loops diferent sizes, sheet 7/3rd try(including binding)/whole';
% Obtain list of all the files in folder
archivos = dir(fullfile(directorio, '*.csv'));
colorg = 'k';

% crate cell to store data tables
tablas = cell(length(archivos), 1);
% go trough files and put each one in a table
for i = 1:length(archivos)
    nombreArchivo = fullfile(directorio, archivos(i).name);
    tabla = readtable(nombreArchivo);
    tablas{i} = tabla;
    Position = tablas{i}.Position;
    nan1 = isnan(Position);
end

color = {'r','b','m','c','g','k','y'};
c=1;

%two "for" loops, j is for unbinding curves (red), k is for binding curves

for j = 1:2:i
    Position = tablas{j}.Position;   %read lts position
    nan1 = isnan(Position);       %identify nan
    pos_no_nan_1 = Position(~nan1);    % eliminate nans from array
    t_tot = tablas{j}.Var1/100;   %time vector
    t_stage2 = linspace(0,max(t_tot),length(pos_no_nan_1))';    %dum vector
    pos_resample_interplj= interp1(t_stage2,pos_no_nan_1,t_tot);   %resample LTS points to match inductive sensor sample rate
    sj = smoothdata(tablas{j}.Induction,'gaussian',50);            %gaussian filter to smooth out curves

    plot(pos_resample_interplj,sj,'.','LineWidth',2,'color','r');    %plotting
    hold on
    xlabel('Displacement (mm)',FontSize=14)
    ylabel('Force (N)',FontSize=14)
    drawnow
    c = c+1;
    hold on
end
c = 1;

 for k = 2:2:i
    Position = tablas{k}.Position;
    nan1 = isnan(Position);
    pos_no_nan_2 = Position(~nan1);
    t_tot = tablas{k}.Var1/100;
    t_stage2 = linspace(0,max(t_tot),length(pos_no_nan_2))';
    pos_resample_interplk= interp1(t_stage2,pos_no_nan_2,t_tot);
    sk = smoothdata(tablas{k}.Induction,'gaussian',50);
    plot(pos_resample_interplk,sk,'.','LineWidth',2,'color','b'); 
    drawnow
    c = c+1;
    hold on
 end
 legend('unbinding','binding','fontsize',14)
