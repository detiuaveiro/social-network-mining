import React from "react";
import { Card, CardHeader, CardBody, Row, Col, FormGroup, Label, Input, Form } from 'reactstrap';
import {FormInputs } from 'components';// used for making the prop types of this component
import { CircularProgressbar} from 'react-circular-progressbar';
import 'emoji-mart/css/emoji-mart.css'
import { Picker } from 'emoji-mart'

class CreateTweet extends React.Component {
  state = {
    text: "",
    nChar: 0,
    emojiShow: false,
    in_Reply: "Timeline",
    tweetid: "",
    allowTweetID: false,
  }
  constructor(props) {
    super(props);
    this.handleSend = this.handleSend.bind(this);
  }

  handleChange = (event) =>{
    this.setState({
      text: event.target.value,
      nChar: event.target.value.length
    })
  }

  addEmoji = (emoji) => {
    this.setState({
      text: this.state.text+emoji.native,
      nChar: this.state.nChar+1
    })
  }

  toogleEmojiState = () => {
    this.setState({
      emojiShow: !this.state.emojiShow
    });
  }

  handleSend = () => {
    this.props.send(this.state.text)
  }

  handleTweetID = event => {
    this.setState({tweetid: event.target.value});
  }

  handleInReply = event => {
    this.setState({
      in_Reply: event.target.value,
      allowTweetID: !this.state.allowTweetID,
    });
  }

  render() {
    return (
      <div>
        {
          this.state.emojiShow
          ? 
          <Row>
            <Col xs={12} md={8}>
              <Card>
                <CardBody>
                  <Row>
                    <Col xs={12} md={12}>
                      <Form>
                        <FormGroup required>
                          <Label for="in_reply_of">Publish Tweet on:</Label>
                          <Row>
                            <FormGroup check className="form-check-radio"> 
                              <Label check>
                                <Input type="radio" name="in_reply" value="Timeline" checked={this.state.in_Reply === 'Timeline'} onChange={this.handleInReply} />{' '}
                                <span className="form-check-sign" />
                                Timeline
                              </Label>
                            </FormGroup>
                            <FormGroup check className="form-check-radio"> 
                              <Label check>
                                <Input type="radio" name="in_reply" value="Tweet" checked={this.state.in_Reply === 'Tweet'} onChange={this.handleInReply} />{' '}
                                <span className="form-check-sign" />
                                Tweet
                              </Label>
                            </FormGroup>
                          </Row>
                        </FormGroup>
                        <FormGroup>
                          <Label for="tweetID">Tweet ID:</Label>
                          <Input type="text" name="tweetID" id="tweetID" value={this.state.tweetid} onChange={this.handleTweetID} disabled={!this.state.allowTweetID}/>
                        </FormGroup>
                      </Form>
                      <FormInputs
                        ncols={["col-md-12"]}
                        proprieties={[
                          {
                            inputProps: {
                              type: "textarea",
                              rows: "5",
                              cols: "80",
                              placeholder: "Write Something ...",
                              value: this.state.text,
                              onChange: this.handleChange
                              }
                          }
                        ]}
                      />
                    </Col>
                  </Row>
                  <Row>
                    <Col xs={3} md={1} style={{height: 30}}>
                      <CircularProgressbar value={this.state.nChar} maxValue={280} text={`${this.state.nChar}/280`} />
                    </Col>
                      <Col xs={5} md={10}>
                      <i class="text-muted float-right far fa-3x fa-smile-wink" onClick={this.toogleEmojiState}></i>
                    </Col>
                    <Col xs={4} md={1}>
                      <i class="text-muted float-right fas fa-3x fa-paper-plane"></i>
                    </Col>
                  </Row>
                </CardBody>
              </Card>
            </Col>
            <Col xs={12} md={4}>
              <Picker
                set="twitter"
                onSelect={this.addEmoji}
              />
            </Col>
          </Row>
        :
        <Row>
          <Col xs={12} md={12}>
            <Card>
              <CardHeader>
                Create Tweet
              </CardHeader>
              <CardBody>
                <Row>
                  <Col xs={12} md={12}>
                    <Form>
                      <FormGroup required>
                        <Label for="in_reply_of">Publish Tweet on:</Label>
                        <Row>
                          <FormGroup check className="form-check-radio"> 
                            <Label check>
                              <Input type="radio" name="in_reply" value="Timeline" checked={this.state.in_Reply === 'Timeline'} onChange={this.handleInReply} />{' '}
                              <span className="form-check-sign" />
                              Timeline
                            </Label>
                          </FormGroup>
                          <FormGroup check className="form-check-radio"> 
                            <Label check>
                              <Input type="radio" name="in_reply" value="Tweet" checked={this.state.in_Reply === 'Tweet'} onChange={this.handleInReply} />{' '}
                              <span className="form-check-sign" />
                              Tweet
                            </Label>
                          </FormGroup>
                        </Row>
                      </FormGroup>
                      <FormGroup>
                        <Label for="tweetID">Tweet ID:</Label>
                        <Input type="text" name="tweetID" id="tweetID" value={this.state.tweetid} onChange={this.handleTweetID} disabled={!this.state.allowTweetID}/>
                      </FormGroup>
                    </Form>
                    <FormInputs
                      ncols={["col-md-12"]}
                      proprieties={[
                        {
                          inputProps: {
                            type: "textarea",
                            rows: "4",
                            cols: "80",
                            placeholder: "Write Something ...",
                            value: this.state.text,
                            onChange: this.handleChange
                            }
                        }
                      ]}
                    />
                  </Col>
                </Row>
                <Row>
                  <Col xs={3} md={1}>
                    <CircularProgressbar style={{ width: 10}} value={this.state.nChar} maxValue={280} text={`${this.state.nChar}/280`} />
                  </Col>
                  <Col xs={5} md={10}>
                    <i class="text-muted float-right far fa-3x fa-smile-wink" onClick={this.toogleEmojiState}></i>
                  </Col>
                  <Col xs={4} md={1}>
                    <i class="text-muted float-right fas fa-3x fa-paper-plane"></i>
                  </Col>
                </Row>
              </CardBody>
            </Card>
          </Col>
        </Row>
        }
        </div>
    );
  }
}



export default CreateTweet;
