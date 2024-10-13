function [] = MatlabFunction() 
format long; 
Q = load('MatriceQ.txt');
R=ones(size(Q,1),1);
Q=horzcat(Q,R);
V= zeros(1,size(Q,1)+1);
V(end)=1;
P=V/Q;
fid=fopen('MatlabFunctionResult.txt','w');
if fid == -1
    error('Impossible d''ouvrir le fichier res.txt');
end
for i=1:length(P) fprintf(fid,'%10.12f',P(i)); fprintf(fid,' '); end
fclose(fid);
 end