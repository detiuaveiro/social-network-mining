import React from "react";
import{ Modal, ModalHeader, ModalBody} from 'reactstrap';
import axios from 'axios';
import {Tweet} from "components";

class RepliesModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        modalTooltips: props.status,
        tweetID: props.tweetID,
        replies: [],
    }
    this.loadReplies = this.loadReplies.bind(this);
  }
  componentDidMount() {
    this.loadReplies()
  }

  loadReplies() {
    axios.get('http://192.168.85.182:5000/twitter/tweets/'+this.props.tweetID+'/replies')
    .then(res => {
      const replies = res.data;
      this.setState({replies});
    })
  }

  componentDidUpdate(prevProps) {
    if (this.props.status !== prevProps.status) {
      this.setState({modalTooltips: this.props.status});
    }
    if (this.props.tweetID !== prevProps.tweetID) {
      this.setState({
        tweetID: this.props.tweetID,
      });
      this.loadReplies()
    }
  }

  render() {
    return (
      <Modal isOpen={this.state.modalTooltips} toggle={this.props.handleClose} size="lg">
        <ModalHeader className="justify-content-center" toggle={this.toggleModalTooltips}>
            Replies
        </ModalHeader>
        <ModalBody>
          {
            (this.state.replies.length===0)
            ?
              <h5 className="text-muted text-center">
                No Replies
              </h5>
            :
              this.state.replies.map(tweet => 
                <Tweet info={tweet}/>
              )}
        </ModalBody>
      </Modal>
    );
  }
}

export default RepliesModal;
