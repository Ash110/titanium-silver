import React,{ Component } from "react";
import { Container,Col,Row,Dropdown } from "react-bootstrap";
// import { Link } from "react-router-dom";

class SignUp extends Component{
    
    constructor(...args){
        super(...args);
        this.state = {
            "acctType":"Student",
            "ID":"",
            "name":"",
            "detailType":"semester",
            "detailValue":"",
            "username":"",
            "password":""
        }
    }

    formSubmit = (e) => {
        e.preventDefault();
        console.log(this.state);
        // Submit to backend and put into database.
    }

    handleChange = (e) => {
        this.setState({
            [e.target.name]:e.target.value
        })
    }

    changeAcctType = (e) => {
        let acctName = e.target.id;
        let detailType = "";

        if(acctName === "Student"){
            detailType="semester";
        }
        else{
            detailType="designation";
        }

        this.setState({
            "acctType":e.target.id,
            "detailType":detailType
        })
    }

    render(){
        return (
            <Container>
                <Row className="justify-content-md-center">
                    <Col xs lg="4">
                        <Container 
                            fluid={true} 
                            style={{marginTop:"10px"}}
                        >
                            <Row>
                                <Col xl={12} lg={12} md={12}>
                                    <h2> Sign Up! </h2>
                                </Col>
                            </Row>
                            <form onSubmit={this.formSubmit}>
                                <Row style={marginTop}>
                                    <Col xl={12} lg={12} md={12}>
                                        <Dropdown>
                                            <Dropdown.Toggle variant="secondary" id="signupAcctDropdown" style={fullWidth}>
                                                Account type {this.state.acctType}
                                            </Dropdown.Toggle>

                                            <Dropdown.Menu style={fullWidth}>
                                                <Dropdown.Item id="Student" onClick={this.changeAcctType}>Student</Dropdown.Item>
                                                <Dropdown.Item id="Teacher" onClick={this.changeAcctType}>Teacher</Dropdown.Item>
                                            </Dropdown.Menu>
                                        </Dropdown>
                                    </Col>
                                </Row>
                                <Row style={marginTop}>
                                    <Col xl={12} lg={12} md={12}>
                                        <span>USN/ID</span>
                                        <input type="text" name="ID" className="form-control" onChange={this.handleChange}/>
                                    </Col>
                                </Row>
                                <Row style={marginTop}>
                                    <Col xl={12} lg={12} md={12}>
                                        <span>Name</span>
                                        <input type="text" name="name" className="form-control" onChange={this.handleChange}/>
                                    </Col>
                                </Row>
                                <Row style={marginTop}>
                                    <Col xl={12} lg={12} md={12}>
                                        <span>Designation/Semester</span>
                                        <input type="text" name="detailValue" className="form-control" onChange={this.handleChange}/>
                                    </Col>
                                </Row>
                                <Row style={marginTop}>
                                    <Col xl={12} lg={12} md={12}>
                                        <span>EmailID</span>
                                        <input type="email" name="username" className="form-control" onChange={this.handleChange}/>
                                    </Col>
                                </Row>
                                <Row style={marginTop}>
                                    <Col xl={12} lg={12} md={12}>
                                        <span>Password</span>
                                        <input type="password" name="password" className="form-control" onChange={this.handleChange}/>
                                    </Col>
                                </Row>
                                <Row style={marginTop}>
                                    <Col xl={12} lg={12} md={12}>
                                        <button className="btn btn-success btn-block" type="submit">Sign Up!</button>
                                    </Col>
                                </Row>
                            </form>
                        </Container>
                    </Col>
                </Row>
            </Container>
        );
    }
}

const fullWidth={
    width:"100%",
    marginTop:"10px"
}

const marginTop = {
    marginTop:"10px"
};

// const marginBottom = {
//     marginBottom:"10px"
// };

export default SignUp;