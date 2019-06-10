import React from "react";
import { Card, CardBody, Row, Col, FormGroup, Label, Input, Form } from 'reactstrap';
import {FormInputs  } from 'components';// used for making the prop types of this component
import { CircularProgressbar} from 'react-circular-progressbar';
import Select from 'react-select';
import { Picker } from 'emoji-mart'

class CreateTweet extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      text: "",
      nChar: 0,
      emojiShow: false,
      in_Reply: "Timeline",
      tweetid: "",
      allowTweetID: false,
      bots: [],
      options: [],
      emptyBots: false,
      emptyText: false,
    }
    this.handleSend = this.handleSend.bind(this);
  }

  componentDidMount() {
    this.setState({
      options: this.props.bots,
      bots: this.props.bots,
    })
  }

  componentDidUpdate(prevProps) {
    if (this.props.bots !== prevProps.bots) {
      this.setState({
        options: this.props.bots,
      });
      
    }
  }

  handleChange = (event) =>{
    this.setState({
      text: event.target.value,
      nChar: event.target.value.length,
    })
    if (this.state.text.length===0){
      this.setState({
        emptyText: false,
      })
    }
  }

  addEmoji = (emoji) => {
    this.setState({
      text: this.state.text+emoji.native,
      nChar: this.state.nChar+2
    })
  }

  toogleEmojiState = () => {
    this.setState({
      emojiShow: !this.state.emojiShow
    });
  }

  handleSend = () => {
    if (this.state.bots.length===0){
      this.setState({emptyBots: true})
    }
    else if (this.state.text.length===0 || this.state.text.length>280){
      this.setState({emptyText: true})
    }
    else {
      let data
      const b = []
      this.state.bots.forEach(function (bot){
        b.push(bot['value'])
      })
      if (this.state.allowTweetID) {
        data = {"in_reply_to_status_id": this.state.tweetid, "status": this.state.text, "bots": b, "timeline": "false"}
      }
      else {
        data = {"status": this.state.text, "bots": b, "timeline": "true"}
      }
      this.props.send(data)
      this.setState({
        text: "",
        nChar: 0,
        emojiShow: false,
        in_Reply: "Timeline",
        tweetid: "",
        allowTweetID: false,
        bots: [],
      })
    }
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

  handleBots = (bots) => {
    this.setState({ bots, emptyBots: false});
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
                          <Label>Bots:</Label>
                            <Select
                              value={this.state.bots}
                              onChange={this.handleBots}
                              options={this.state.options}
                              isMulti
                              isSearchable
                              placeholder="Add Bots"
                              styles={{
                                control: (provided,state) => ({
                                  ...provided,
                                  borderRadius: 30,
                                  borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                                  boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                                  '&:hover': {
                                    borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                                    boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                                  },
                                }),
                                multiValue: (provided, state) => ({
                                  ...provided,
                                  backgroundColor: "#f96332",
                                  color: "white",
                                  borderRadius: 30,
                                }),
                              }}
                              className="primary"

                            />
                            <div hidden={!this.state.emptyBots} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                                Field can't be empty!
                            </div>
                        </FormGroup>
                        <FormGroup required>
                          <Label for="in_reply_of">Method:</Label>
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
                                <Input type="radio" name="in_reply" value="Reply" checked={this.state.in_Reply === 'Reply'} onChange={this.handleInReply} />{' '}
                                <span className="form-check-sign" />
                                Reply
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
                            label: "Text:",
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
                      <div hidden={!this.state.emptyText} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                        Field can't be empty or have more than 280 characters!
                      </div>
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
                      <div>
                        <i class="text-muted float-right far fa-3x fa-paper-plane" onClick={this.handleSend}></i>
                      </div>
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
              <CardBody>
                <Row>
                  <Col xs={12} md={12}>
                    <Form>
                      <FormGroup required>
                        <Label>Bots:</Label>
                          <Select
                            value={this.state.bots}
                            onChange={this.handleBots}
                            options={this.state.options}
                            isMulti
                            isSearchable
                            placeholder="Add Bots"
                            styles={{
                              control: (provided,state) => ({
                                ...provided,
                                borderRadius: 30,
                                borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                                boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                                '&:hover': {
                                  borderColor: state.isFocused ? "#f96332" : "#E3E3E3",
                                  boxShadow: state.isFocused ? "#f96332" : "#E3E3E3",
                                },
                              }),
                              multiValue: (provided, state) => ({
                                ...provided,
                                backgroundColor: "#f96332",
                                color: "white",
                                borderRadius: 30,
                              }),
                            }}
                            className="primary"

                          />
                          <div hidden={!this.state.emptyBots} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                              Field can't be empty!
                          </div>
                      </FormGroup>
                      <FormGroup required>
                        <Label for="in_reply_of">Method:</Label>
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
                              <Input type="radio" name="in_reply" value="Reply" checked={this.state.in_Reply === 'Reply'} onChange={this.handleInReply} />{' '}
                              <span className="form-check-sign" />
                              Reply
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
                          label: "Text:",
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
                    <div hidden={!this.state.emptyText} className="alert-danger mt-2 p-2" style={{borderRadius: 30}}>
                      Field can't be empty or have more than 280 characters!
                    </div>
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
                      <i class="text-muted float-right far fa-3x fa-paper-plane" onClick={this.handleSend}></i>
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
