import React from 'react';
import { Link } from 'react-router-dom';

class HomeHeader extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = { show: true}
        this.toggleHeader = this.toggleHeader.bind(this);
    }

    toggleHeader = () => {
        const {show} = this.state;
        this.setState({show: !show})
    }
    
    render() {
        const show = this.state.show;
        
        if (show) {
            return (
                <header id="header" class="header-area header-sticky background-header">
                    <div class="container">
                        <div class="row">
                            <div class="col-12">
                                <nav class="main-nav">
                                    <Link class="logo" to="/">Intrusion Tracker</Link>
                                    <ul class="nav">
                                        <li class="scroll-to-section"><Link class="active" to="/">Home</Link></li>
                                        <li class="scroll-to-section"><a href="#about">About</a></li>
                                        <li class="scroll-to-section"><a href="#services">Services</a></li>
                                        <li class="scroll-to-section"><a href="#contact-us">Contact Us</a></li>
                                        <li class="scroll-to-section" class="sign-button"><Link to="/login"><i class="fas fa-user fa-md" style={{marginLeft: "0px", marginRight: "5px"}}></i> Login</Link></li>
                                        <li class="scroll-to-section"><Link to="/signup">Sign Up</Link></li>
                                    </ul>
                                    <a class='menu-trigger'>
                                        <span>Menu</span>
                                    </a>
                                </nav>
                            </div>
                        </div>
                    </div>
                </header>        
            )
        } else {
            return (
                <div></div>
            );
        }
    }
}

export default HomeHeader;