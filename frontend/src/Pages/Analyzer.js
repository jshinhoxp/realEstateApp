import React from "react";
import "../css/Pages.css";

export default function Projects() {
    return (
		<div className="pages">
			<h1> Coding Projects </h1>
			<ul>
				<li> <h3> Personal Website </h3> </li>
					<p> Consolidates work of a true professional in one single-page application. Made with React Framework. Hosted via Google Domain. </p>
				<li> <h3> Real Estate Estimator App </h3> </li>
					<p> Uses machine learning to estimate the property value and potential renovation costs through visual and public data. </p>
				<li> <h3> Stock Market Estimator App </h3></li>
					<p> Auto Trading Bot that uses a machine learning model that utilizes basic, yet complex algorithms to predict future stock market movements. </p>
				<li> <h3> Robinhood Tax Estimator App </h3> </li>
					<p> To calculate current and projected dividend and stock earnings to assist in estimating tax liability </p>
				<li> TO DO LIST </li>
			</ul>
		</div>
  );
};