clc; clear; close;
filename = 'ecgDataArray.csv';
ecgData = csvread(filename);
[r c] = size(ecgData);

figure(1)
rows=4;
subplot(rows,1,1)
plot(ecgData(108,:))
subplot(rows,1,2)
plot(ecgData(110,:))
subplot(rows,1,3)
plot(ecgData(152,:))
subplot(rows,1,4)
plot(ecgData(154,:))

figure(2)
subplot(rows,1,1)
plot(ecgData(107,:))
subplot(rows,1,2)
plot(ecgData(109,:))
subplot(rows,1,3)
plot(ecgData(150,:))
subplot(rows,1,4)
plot(ecgData(152,:))

figure(3)
y1 = ecgData(107,:)-ecgData(153,:)
plot(y1)
