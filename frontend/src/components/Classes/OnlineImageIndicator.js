import React from "react";
import Image from "react-bootstrap/Image";
import placeholder_user from "../../assets/images/placeholder_user.png";
import classes from "./OnlineImageIndicator.module.scss";

const OnlineImageIndicator = (props) => {
  const isOnline = Math.random() < 0.5;
  const imageSrc = props.profile_pic ? props.profile_pic : placeholder_user;

  const onlineColorIndicator = { false: "red", true: "green" };
  return (
    <div
      className={classes.profileImgWrapper}
      style={{ "--after-bg-color": onlineColorIndicator[isOnline] }}
    >
      <Image src={imageSrc} roundedCircle className={classes.profileImg} />
    </div>
  );
};

export default OnlineImageIndicator;
