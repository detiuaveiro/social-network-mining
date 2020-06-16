import React, { Component } from "react";

import CountUp from 'react-countup';
import VisibilitySensor from 'react-visibility-sensor';

import './styles/css/bootstrap.min.css';
import './styles/css/animate.css';
import './styles/css/magnific-popup.css';
import './styles/css/slick.css';
import './styles/css/font-awesome.min.css';
import './styles/css/themify-icons.css';
import './styles/css/ionicons.min.css';
import './styles/css/responsive.css';

import './styles/style.css'
import './styles/js/active'

import main_img from './styles/img/bg-img/welcome-img.png'
import special_img from './styles/img/bg-img/special.png'

import app_1 from './styles/img/scr-img/app-1.jpg'
import app_2 from './styles/img/scr-img/app-2.jpg'
import app_3 from './styles/img/scr-img/app-3.jpg'
import app_4 from './styles/img/scr-img/app-4.jpg'
import app_5 from './styles/img/scr-img/app-5.jpg'

import escal from './styles/img/team-img/team-1.png'
import rafa from './styles/img/team-img/team-2.png'
import ds from './styles/img/team-img/team-3.png'
import fagoti from './styles/img/team-img/team-4.png'


class LandingLayout extends Component {
    render() {
        return (
            <div>
                <header className="header_area animated">
                    <div className="container-fluid">
                        <div className="row align-items-center">
                            <div className="col-12 col-lg-10">
                                <div className="menu_area">
                                    <nav className="navbar navbar-expand-lg navbar-light">
                                        <a className="navbar-brand" href="#">Minerva</a>
                                        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#ca-navbar" aria-controls="ca-navbar" aria-expanded="false" aria-label="Toggle navigation"><span className="navbar-toggler-icon"></span></button>
                                        <div className="collapse navbar-collapse" id="ca-navbar">
                                            <ul className="navbar-nav ml-auto" id="nav">
                                                <li className="nav-item active"><a className="nav-link" href="#home">Home</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#about">About</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#features">Features</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#screenshot">Screenshot</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#team">Team</a></li>
                                            </ul>
                                        </div>
                                    </nav>
                                </div>
                            </div>
                            <div className="col-12 col-lg-2">
                                <div className="sing-up-button d-none d-lg-block">
                                    <a href="/dash" >Dashboard</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </header>


                <section className="wellcome_area clearfix" id="home">
                    <div className="container h-100">
                        <div className="row h-100 align-items-center">
                            <div className="col-12 col-md-12 col-sm-12">
                                <div className="wellcome-heading">
                                    <h2>Minerva</h2>
                                    <h3>M</h3>
                                    <p>Social Network Mining</p>
                                </div>
                                <div className="get-start-area">
                                    <button className="submit" href="/dash">Go to Dashboard</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="welcome-thumb wow fadeInDown" data-wow-delay="0.5s">
                        <img src={main_img} alt="" style={{ maxWidth: "700px" }}></img>
                    </div>
                </section>


                <section className="special-area bg-white section_padding_100" id="about">
                    <div className="special_description_area mt-150">
                        <div className="container">
                            <div className="row">
                                <div className="col-lg-6">
                                    <div className="special_description_img">
                                        <img src={special_img} alt=""></img>
                                    </div>
                                </div>
                                <div className="col-lg-6 col-xl-5 ml-xl-auto">
                                    <div className="special_description_content">
                                        <h2>Get a feel for the flow of information!</h2>
                                        <p>Minetwork is a tool for analyzing the connections observable on social networks. It allows you to study the connections between people, how the information gets passed around between users and how news and media get propagated throughout.</p>
                                        <div className="app-download-area">
                                            <div className="app-download-btn wow fadeInDown" data-wow-delay="0.4s">
                                                <a href="/dash">
                                                    <i className="fa fa-globe"></i>
                                                    <p className="mb-0"><span>available as</span> a Web-App</p>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="container">
                        <div className="row">
                            <div className="col-12">
                                <div className="section-heading text-center">
                                    <h2>How it Works</h2>
                                    <div className="line-shape"></div>
                                </div>
                            </div>
                        </div>

                        <div className="row">
                            <div className="col-12 col-md-4">
                                <div className="single-special text-center wow fadeInUp" data-wow-delay="0.2s">
                                    <div className="single-icon">
                                        <i className="fas fa-robot" aria-hidden="true"></i>
                                    </div>
                                    <h4>Deploy Bots</h4>
                                    <p>Create and deploy bots and send them out on their way to scour the social network for information. Tweak policies to customize the bots' behaviours</p>
                                </div>
                            </div>
                            <div className="col-12 col-md-4">
                                <div className="single-special text-center wow fadeInUp" data-wow-delay="0.4s">
                                    <div className="single-icon">
                                        <i className="fas fa-search" aria-hidden="true"></i>
                                    </div>
                                    <h4>Bots Gather Information</h4>
                                    <p>The bots attempt to infiltrate the inner circles of both private and public accounts in order to build their own hub of followers and followees</p>
                                </div>
                            </div>
                            <div className="col-12 col-md-4">
                                <div className="single-special text-center wow fadeInUp" data-wow-delay="0.6s">
                                    <div className="single-icon">
                                        <i className="fas fa-chart-bar" aria-hidden="true"></i>
                                    </div>
                                    <h4>Analyze Results</h4>
                                    <p>You'll be presented with several statistics, a graph of connections, the flow of information and a customizable report of results</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <section className="awesome-feature-area bg-white section_padding_0_50 clearfix" id="features">
                    <div className="container">
                        <div className="row">
                            <div className="col-12">
                                <div className="section-heading text-center">
                                    <h2>Awesome Features</h2>
                                    <div className="line-shape"></div>
                                </div>
                            </div>
                        </div>

                        <div className="row">
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="fas fa-brain" aria-hidden="true"></i>
                                    <h5>Human-like Bots</h5>
                                    <p>Create and customize human-like bots, able to follow users, tweet and even engage in meaningful conversations.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="far fa-smile-beam" aria-hidden="true"></i>
                                    <h5>Easy-to-use</h5>
                                    <p>Explore our clean and easy to use platforms, available both in-browser and as an android app.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="fas fa-pencil-alt" aria-hidden="true"></i>
                                    <h5>Customizable Reports</h5>
                                    <p>Automatically generate cutstomizable reports by specifying what type of information to include.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="fas fa-chart-line" aria-hidden="true"></i>
                                    <h5>In-depth Data</h5>
                                    <p>Analyze a wide range of up-to-date graphs, logs and charts to study anomalies with the transmission of data.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="fas fa-project-diagram" aria-hidden="true"></i>
                                    <h5>Network Visualization</h5>
                                    <p>Visualize and scour the resulting network graph of connections between users and data.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="fas fa-user-tag" aria-hidden="true"></i>
                                    <h5>Policy Definition</h5>
                                    <p>Define customizable tags and assign them to bots so that they specialize in following and scraping for users that fit into those parameters.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <section className="awesome-feature-area bg-white section_padding_0_50 clearfix" id="features">
                    <div className="container">
                        <div className="row">
                            <div className="col-12">
                                <div className="section-heading text-center">
                                    <h2>Available For</h2>
                                    <div className="line-shape"></div>
                                </div>
                            </div>
                        </div>

                        <div className="row">
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="fab fa-twitter" aria-hidden="true"></i>
                                    <h5>Twitter</h5>
                                    <p>Build and analyze a network of followers, the flow of tweets and how data is spread through one of the most viral social networks.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <div className="video-section">
                    <div className="container">
                        <div className="row">
                            <div className="col-12">
                                <div className="video-area">
                                    <div className="video-play-btn">
                                        <a href="https://www.youtube.com/watch?v=f5BBJ4ySgpo" className="video_btn"><i className="fa fa-play" aria-hidden="true"></i></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>


                <section className="cool_facts_area clearfix">
                    <div className="container">
                        <div className="row">
                            <div className="col-12 col-md-3 col-lg-3">
                                <div className="single-cool-fact d-flex justify-content-center wow fadeInUp" data-wow-delay="0.2s">
                                    <div className="counter-area">
                                        <h3>
                                            <span className="counter">
                                                3
                                            </span>
                                        </h3>
                                    </div>
                                    <div className="cool-facts-content">
                                        <i className="fas fa-robot"></i>
                                        <p>BOTS</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-3 col-lg-3">
                                <div className="single-cool-fact d-flex justify-content-center wow fadeInUp" data-wow-delay="0.4s">
                                    <div className="counter-area">
                                        <h3>
                                            <span className="counter">
                                                >300K
                                            </span>
                                        </h3>
                                    </div>
                                    <div className="cool-facts-content">
                                        <i className="fas fa-users"></i>
                                        <p>USERS</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-3 col-lg-3">
                                <div className="single-cool-fact d-flex justify-content-center wow fadeInUp" data-wow-delay="0.6s">
                                    <div className="counter-area">
                                        <h3>
                                            <span className="counter">
                                                >500K
                                            </span>
                                        </h3>
                                    </div>
                                    <div className="cool-facts-content">
                                        <i className="far fa-comment-alt"></i>
                                        <p>TWEETS</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-3 col-lg-3">
                                <div className="single-cool-fact d-flex justify-content-center wow fadeInUp" data-wow-delay="0.8s">
                                    <div className="counter-area">
                                        <h3>
                                            <span className="counter">
                                                >1M
                                            </span>
                                        </h3>
                                    </div>
                                    <div className="cool-facts-content">
                                        <i className="fas fa-project-diagram"></i>
                                        <p>RELATIONS</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>

                <section className="our-monthly-membership section_padding_50 clearfix">
                    <div className="container">
                        <div className="row align-items-center">
                            <div className="col-md-8">
                                <div className="membership-description">
                                    <h2>Try it out right now!</h2>
                                    <p>Check out one of our platforms and start gaining insight today!</p>
                                </div>
                            </div>

                            <div className="app-download-area col-md-4 col-sm-12">
                                <div className="app-download-btn2 wow fadeInDown" data-wow-delay="0.4s">
                                    <a href="/dash">
                                        <i className="fa fa-globe"></i>
                                        <p className="mb-0"><span>available as</span> a Web-App</p>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <section className="our-Team-area bg-white section_padding_100_50 clearfix" id="team">
                    <div className="container">
                        <div className="row">
                            <div className="col-12 text-center">
                                <div className="section-heading">
                                    <h2>Our Team</h2>
                                    <div className="line-shape"></div>
                                </div>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-12 col-md-6 col-lg-3">
                                <div className="single-team-member">
                                    <div className="member-image">
                                        <img src={escal} alt="" />
                                        <div className="team-hover-effects">
                                            <div className="team-social-icon">
                                                <a href="https://github.com/oEscal"><i className="fa fa-github" aria-hidden="true"></i></a>
                                                <a href="https://www.linkedin.com/in/pedro-escaleira-b9b39115b/"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="member-text">
                                        <h4>Pedro Escaleira</h4>
                                        <p>88821</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-6 col-lg-3">
                                <div className="single-team-member">
                                    <div className="member-image">
                                        <img src={ds} alt="" />
                                        <div className="team-hover-effects">
                                            <div className="team-social-icon">
                                                <a href="https://github.com/Rafaelyot"><i className="fa fa-github" aria-hidden="true"></i></a>
                                                <a href="https://www.linkedin.com/in/rafael-sim%C3%B5es-60958b173/"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="member-text">
                                        <h4>Diogo Silva</h4>
                                        <p>89348</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-6 col-lg-3">
                                <div className="single-team-member">
                                    <div className="member-image">
                                        <img src={rafa} alt="" />
                                        <div className="team-hover-effects">
                                            <div className="team-social-icon">
                                                <a href="https://github.com/HerouFenix"><i className="fa fa-github" aria-hidden="true"></i></a>
                                                <a href="https://www.linkedin.com/in/diogosilvads/"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="member-text">
                                        <h4>Rafael Simões</h4>
                                        <p>88984</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-6 col-lg-3">
                                <div className="single-team-member">
                                    <div className="member-image">
                                        <img src={fagoti} alt="" />
                                        <div className="team-hover-effects">
                                            <div className="team-social-icon">
                                                <a href="https://github.com/DrPunpun"><i className="fa fa-github" aria-hidden="true"></i></a>
                                                <a href="https://www.linkedin.com/in/pedromroliveirapt/"><i className="fa fa-linkedin" aria-hidden="true"></i></a>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="member-text">
                                        <h4>Pedro Oliveira</h4>
                                        <p>89156</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <footer className="footer-social-icon text-center section_padding_70 clearfix">
                    <div className="footer-text">
                        <h2>Minerva</h2>
                    </div>
                    <div className="footer-social-icon">
                        <a href="#"><i className="fa fa-facebook" aria-hidden="true"></i></a>
                        <a href="#"><i className="fa fa-twitter" aria-hidden="true"></i></a>
                        <a href="#"> <i className="fa fa-instagram" aria-hidden="true"></i></a>
                        <a href="#"><i className="fa fa-google-plus" aria-hidden="true"></i></a>
                    </div>
                    <div className="copyright-text">
                        <p>Grupo 14, Projeto de Informática. Universidade de Aveiro, 2019-2020</p>
                    </div>
                </footer>
            </div>
        );
    }
}

export default LandingLayout;
