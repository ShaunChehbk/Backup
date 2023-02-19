import React from "react"

import CardList from "./CardList"

const Refresh = ({refresh=()=>{console.log("refresh")}}) => {
// const Refresh = (refresh=()=>{console.log("refresh")}) => {
    return (
        <button
            onClick={refresh}
        >
            Refresh
        </button>
    )
}

class CardContainer extends React.Component {
    state = {
        words: [
        ]
    }
    componentDidMount() {
        fetch("http://47.104.147.223:8080/en/random_untouched")
            .then(response => response.json())
            .then(data => {
                this.setState({
                    words: data
                })
            })
    }
    // componentDidMount() {
    //     fetch("http://47.104.147.223:8080/en/random")
    //         .then(response => {
    //             var data = response.json()
    //             console.log(data)
    //             this.setState({
    //                 words: data
    //             })
    //         })
    // }
    rateWord = (word, rate) => {
        console.log(word, rate)
        fetch("http://47.104.147.223:8080/en/touch", {
            method: "POST", mode: "cors", headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({word: word, rating: rate})
        })
            .then(response => console.log(response.json()))
    }
    refresh = () => {
        fetch("http://47.104.147.223:8080/en/random_untouched")
        .then(response => response.json())
        .then(data => {
            this.setState({
                words: data
            })
        })
    }
    render() {
        return (
            <div>
                <Refresh 
                    refresh={this.refresh}/>
                <CardList 
                    words={this.state.words}
                    rateWordProps={this.rateWord}
                />
            </div>
        )
    }
}

export default CardContainer
