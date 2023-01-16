import React from "react";
import "../css/Footer.css"
import * as AiIcons from "react-icons/ai"

export default function Footer() {
	return (
		<div className="footer">
			<div className="container1">
				<div className="contact"> 
				<h2> CONTACT </h2>
					<ul className="contact-icons">
						<li><AiIcons.AiOutlineMail />
							Email </li>
						<li><AiIcons.AiOutlineFacebook />
							<a href="https://www.facebook.com/jshinhoxp">
							Facebook </a> </li>
						<li><AiIcons.AiOutlineInstagram />
							<a href="https://www.instagram.com/jshinhoxp">
							Instagram </a> </li>
						<li><AiIcons.AiOutlineTwitter />
							<a href="https://www.twitter.com/jshinhoxp">
							Twitter </a> </li>
						<li><AiIcons.AiOutlineLinkedin />
							<a href="https://linkedin.com/in/jungshinho">
							LinkedIn </a> </li> 
					</ul>
				</div>
				<div className="subscribe">
					<p>Sean Jung is an mechanical engineer and computer enthusiast. He brings his best in all his endeavors! Machine learning production.</p>
					<h3> Subscribe to his latest email Newsletter! </h3>
					<h3> Email Address </h3>
					<input type="text" className="email-list"/> <br />
					<button type="button">Subscribe</button>
				</div>
			</div>
			<div className="container2"> 
				<div className="rights">
					| © 2023 Sean Jung LLC | All Rights Reserved | Privacy | Terms & Conditions |
				</div>
			</div>
		</div>
    )
};