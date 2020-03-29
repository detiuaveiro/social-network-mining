import React, { Component, Suspense } from "react";

import CountUp from 'react-countup';
import VisibilitySensor from 'react-visibility-sensor';

import './styles/css/bootstrap.min.css';
import './styles/css/animate.css';
import './styles/css/magnific-popup.css';
import './styles/css/slick.css';
import './styles/css/font-awesome.min.css';
import './styles/css/themify-icons.css';
import './styles/css/ionicons.min.css';
import './styles/css/responsive.css'

import './styles/style.css'

import main_img from './styles/img/bg-img/welcome-img.png'
import special_img from './styles/img/bg-img/special.png'

import app_1 from './styles/img/scr-img/app-1.jpg'
import app_2 from './styles/img/scr-img/app-2.jpg'
import app_3 from './styles/img/scr-img/app-3.jpg'
import app_4 from './styles/img/scr-img/app-4.jpg'
import app_5 from './styles/img/scr-img/app-5.jpg'

import escal from './styles/img/team-img/team-1.jpg'
import rafa from './styles/img/team-img/team-2.jpg'
import ds from './styles/img/team-img/team-3.jpg'
import fagoti from './styles/img/team-img/team-4.jpg'


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
                                        <a className="navbar-brand" href="#">Minetwork</a>
                                        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#ca-navbar" aria-controls="ca-navbar" aria-expanded="false" aria-label="Toggle navigation"><span className="navbar-toggler-icon"></span></button>
                                        <div className="collapse navbar-collapse" id="ca-navbar">
                                            <ul className="navbar-nav ml-auto" id="nav">
                                                <li className="nav-item active"><a className="nav-link" href="#home">Home</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#about">About</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#features">Features</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#screenshot">Screenshot</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#pricing">Pricing</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#testimonials">Testimonials</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#team">Team</a></li>
                                                <li className="nav-item"><a className="nav-link" href="#contact">Contact</a></li>
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
                            <div className="col-12 col-md">
                                <div className="wellcome-heading">
                                    <h2>Minetwork</h2>
                                    <h3>M</h3>
                                    <p>Social Network Mining</p>
                                </div>
                                <div className="get-start-area">
                                    <button className="submit">Go to Dashboard</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="welcome-thumb wow fadeInDown" data-wow-delay="0.5s">
                        <img src={main_img} alt=""></img>
                    </div>
                </section>


                <section className="special-area bg-white section_padding_100" id="about">
                    <div className="container">
                        <div className="row">
                            <div className="col-12">
                                <div className="section-heading text-center">
                                    <h2>Why Is It Special</h2>
                                    <div className="line-shape"></div>
                                </div>
                            </div>
                        </div>

                        <div className="row">
                            <div className="col-12 col-md-4">
                                <div className="single-special text-center wow fadeInUp" data-wow-delay="0.2s">
                                    <div className="single-icon">
                                        <i className="ti-mobile" aria-hidden="true"></i>
                                    </div>
                                    <h4>Easy to use</h4>
                                    <p>We build pretty complex tools and this allows us to take designs and turn them into functional quickly and easily</p>
                                </div>
                            </div>
                            <div className="col-12 col-md-4">
                                <div className="single-special text-center wow fadeInUp" data-wow-delay="0.4s">
                                    <div className="single-icon">
                                        <i className="ti-ruler-pencil" aria-hidden="true"></i>
                                    </div>
                                    <h4>Powerful Design</h4>
                                    <p>We build pretty complex tools and this allows us to take designs and turn them into functional quickly and easily</p>
                                </div>
                            </div>
                            <div className="col-12 col-md-4">
                                <div className="single-special text-center wow fadeInUp" data-wow-delay="0.6s">
                                    <div className="single-icon">
                                        <i className="ti-settings" aria-hidden="true"></i>
                                    </div>
                                    <h4>Customizability</h4>
                                    <p>We build pretty complex tools and this allows us to take designs and turn them into functional quickly and easily</p>
                                </div>
                            </div>
                        </div>
                    </div>
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
                                        <h2>Our Best Propositions for You!</h2>
                                        <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco.</p>
                                        <div className="app-download-area">
                                            <div className="app-download-btn wow fadeInUp" data-wow-delay="0.2s">
                                                <a href="#">
                                                    <i className="fa fa-android"></i>
                                                    <p className="mb-0"><span>available on</span> Google Store</p>
                                                </a>
                                            </div>
                                            <div className="app-download-btn wow fadeInDown" data-wow-delay="0.4s">
                                                <a href="#">
                                                    <i className="fa fa-apple"></i>
                                                    <p className="mb-0"><span>available on</span> Apple Store</p>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
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
                                    <i className="ti-user" aria-hidden="true"></i>
                                    <h5>Awesome Experience</h5>
                                    <p>Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="ti-pulse" aria-hidden="true"></i>
                                    <h5>Fast and Simple</h5>
                                    <p>Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="ti-dashboard" aria-hidden="true"></i>
                                    <h5>Clean Code</h5>
                                    <p>Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="ti-palette" aria-hidden="true"></i>
                                    <h5>Perfect Design</h5>
                                    <p>Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="ti-crown" aria-hidden="true"></i>
                                    <h5>Best Industry Leader</h5>
                                    <p>Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
                                </div>
                            </div>
                            <div className="col-12 col-sm-6 col-lg-4">
                                <div className="single-feature">
                                    <i className="ti-headphone" aria-hidden="true"></i>
                                    <h5>24/7 Online Support</h5>
                                    <p>Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
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
                                                <CountUp start={0} end={100} redraw={true}>
                                                    {({ countUpRef, start }) => (
                                                        <VisibilitySensor onChange={start} delayedCall>
                                                            <span ref={countUpRef} />
                                                        </VisibilitySensor>
                                                    )}
                                                </CountUp>
                                            </span>
                                        </h3>
                                    </div>
                                    <div className="cool-facts-content">
                                        <i className="ion-arrow-down-a"></i>
                                        <p>APP <br /> DOWNLOADS</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-3 col-lg-3">
                                <div className="single-cool-fact d-flex justify-content-center wow fadeInUp" data-wow-delay="0.4s">
                                    <div className="counter-area">
                                        <h3>
                                            <span className="counter">
                                                <CountUp start={0} end={100} redraw={true}>
                                                    {({ countUpRef, start }) => (
                                                        <VisibilitySensor onChange={start} delayedCall>
                                                            <span ref={countUpRef} />
                                                        </VisibilitySensor>
                                                    )}
                                                </CountUp>
                                            </span>
                                        </h3>
                                    </div>
                                    <div className="cool-facts-content">
                                        <i className="ion-happy-outline"></i>
                                        <p>Happy <br /> Clients</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-3 col-lg-3">
                                <div className="single-cool-fact d-flex justify-content-center wow fadeInUp" data-wow-delay="0.6s">
                                    <div className="counter-area">
                                        <h3>
                                            <span className="counter">
                                                <CountUp start={0} end={100} redraw={true}>
                                                    {({ countUpRef, start }) => (
                                                        <VisibilitySensor onChange={start} delayedCall>
                                                            <span ref={countUpRef} />
                                                        </VisibilitySensor>
                                                    )}
                                                </CountUp>
                                            </span>
                                        </h3>
                                    </div>
                                    <div className="cool-facts-content">
                                        <i className="ion-person"></i>
                                        <p>ACTIVE <br />ACCOUNTS</p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-3 col-lg-3">
                                <div className="single-cool-fact d-flex justify-content-center wow fadeInUp" data-wow-delay="0.8s">
                                    <div className="counter-area">
                                        <h3>
                                            <span className="counter">
                                                <CountUp start={0} end={100} redraw={true}>
                                                    {({ countUpRef, start }) => (
                                                        <VisibilitySensor onChange={start} delayedCall>
                                                            <span ref={countUpRef} />
                                                        </VisibilitySensor>
                                                    )}
                                                </CountUp>
                                            </span>
                                        </h3>
                                    </div>
                                    <div className="cool-facts-content">
                                        <i className="ion-ios-star-outline"></i>
                                        <p>TOTAL <br />APP RATES</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <section className="app-screenshots-area bg-white section_padding_0_100 clearfix" id="screenshot">
                    <div className="container">
                        <div className="row">
                            <div className="col-12 text-center">
                                <div className="section-heading">
                                    <h2>App Screenshots</h2>
                                    <div className="line-shape"></div>
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
                                    <h2>Join our Monthly Membership</h2>
                                    <p>Find the perfect plan for you — 100% satisfaction guaranteed.</p>
                                </div>
                            </div>
                            <div className="col-md-4">
                                <div className="get-started-button wow bounceInDown" data-wow-delay="0.5s">
                                    <a href="#">Get Started</a>
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
                                                <a href="#"><i className="fa fa-facebook" aria-hidden="true"></i></a>
                                                <a href="#"><i className="fa fa-twitter" aria-hidden="true"></i></a>
                                                <a href="#"><i className="fa fa-google-plus" aria-hidden="true"></i></a>
                                                <a href="#"> <i className="fa fa-instagram" aria-hidden="true"></i></a>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="member-text">
                                        <h4>Pedro Escaleira</h4>
                                        <p></p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-6 col-lg-3">
                                <div className="single-team-member">
                                    <div className="member-image">
                                        <img src={ds} alt="" />
                                        <div className="team-hover-effects">
                                            <div className="team-social-icon">
                                                <a href="#"><i className="fa fa-facebook" aria-hidden="true"></i></a>
                                                <a href="#"><i className="fa fa-twitter" aria-hidden="true"></i></a>
                                                <a href="#"><i className="fa fa-google-plus" aria-hidden="true"></i></a>
                                                <a href="#"> <i className="fa fa-instagram" aria-hidden="true"></i></a>
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
                                                <a href="#"><i className="fa fa-facebook" aria-hidden="true"></i></a>
                                                <a href="#"><i className="fa fa-twitter" aria-hidden="true"></i></a>
                                                <a href="#"><i className="fa fa-google-plus" aria-hidden="true"></i></a>
                                                <a href="#"> <i className="fa fa-instagram" aria-hidden="true"></i></a>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="member-text">
                                        <h4>Rafael Simões</h4>
                                        <p></p>
                                    </div>
                                </div>
                            </div>
                            <div className="col-12 col-md-6 col-lg-3">
                                <div className="single-team-member">
                                    <div className="member-image">
                                        <img src={fagoti} alt="" />
                                        <div className="team-hover-effects">
                                            <div className="team-social-icon">
                                                <a href="#"><i className="fa fa-facebook" aria-hidden="true"></i></a>
                                                <a href="#"><i className="fa fa-twitter" aria-hidden="true"></i></a>
                                                <a href="#"><i className="fa fa-google-plus" aria-hidden="true"></i></a>
                                                <a href="#"> <i className="fa fa-instagram" aria-hidden="true"></i></a>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="member-text">
                                        <h4>Pedro Oliveira</h4>
                                        <p></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <section className="footer-contact-area section_padding_100 clearfix" id="contact">
                    <div className="container">
                        <div className="row">
                            <div className="col-md-6">
                                <div className="section-heading">
                                    <h2>Get in touch with us!</h2>
                                    <div className="line-shape"></div>
                                </div>
                                <div className="footer-text">
                                    <p>We'll send you epic weekly blogs, whitepapers and things to make your app startup thrive, all FREE!</p>
                                </div>
                                <div className="address-text">
                                    <p><span>Address:</span> 40 Baria Sreet 133/2 NewYork City, US</p>
                                </div>
                                <div className="phone-text">
                                    <p><span>Phone:</span> +11-225-888-888-66</p>
                                </div>
                                <div className="email-text">
                                    <p><span>Email:</span> info.deercreative@gmail.com</p>
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div className="contact_from">
                                    <form action="#" method="post">
                                        <div className="contact_input_area">
                                            <div className="row">
                                                <div className="col-md-12">
                                                    <div className="form-group">
                                                        <input type="text" className="form-control" name="name" id="name" placeholder="Your Name" required />
                                                    </div>
                                                </div>
                                                <div className="col-md-12">
                                                    <div className="form-group">
                                                        <input type="email" className="form-control" name="email" id="email" placeholder="Your E-mail" required />
                                                    </div>
                                                </div>
                                                <div className="col-12">
                                                    <div className="form-group">
                                                        <textarea name="message" className="form-control" id="message" cols="30" rows="4" placeholder="Your Message *" required></textarea>
                                                    </div>
                                                </div>
                                                <div className="col-12">
                                                    <button type="submit" className="btn submit-btn">Send Now</button>
                                                </div>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>


                <footer className="footer-social-icon text-center section_padding_70 clearfix">
                    <div className="footer-text">
                        <h2>Ca.</h2>
                    </div>
                    <div className="footer-social-icon">
                        <a href="#"><i className="fa fa-facebook" aria-hidden="true"></i></a>
                        <a href="#"><i className="fa fa-twitter" aria-hidden="true"></i></a>
                        <a href="#"> <i className="fa fa-instagram" aria-hidden="true"></i></a>
                        <a href="#"><i className="fa fa-google-plus" aria-hidden="true"></i></a>
                    </div>
                    <div className="footer-menu">
                        <nav>
                            <ul>
                                <li><a href="#">About</a></li>
                                <li><a href="#">Terms &amp; Conditions</a></li>
                                <li><a href="#">Privacy Policy</a></li>
                                <li><a href="#">Contact</a></li>
                            </ul>
                        </nav>
                    </div>
                    <div className="copyright-text">
                        <p>Copyright ©2017 Ca. Designed by <a href="https://colorlib.com" target="_blank">Colorlib</a></p>
                    </div>
                </footer>
            </div>
        );
    }
}

export default LandingLayout;
