read -p "Enter Image: " image
read -p "Enter name: " name

docker run -it --name ${name} \
--env DISPLAY=${DISPLAY} \
--env="QT_X11_NO_MITSHM=1" \
--net=host --ipc=host \
--volume ${HOME}/Documents/gt_domain:/root/gt_domain \
--volume /tmp/.X11-unix:/tmp/.X11-unix \
--volume ~/.Xauthority:/root/.Xauthority \
--device=/dev/video0 \
--device=/dev/input \
--device=/dev/dri/card0 \
${image}
