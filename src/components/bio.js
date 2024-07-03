import * as React from "react"
import { useStaticQuery, graphql } from "gatsby"

const Bio = () => {
  const data = useStaticQuery(graphql`
    query BioQuery {
      site {
        siteMetadata {
          author {
            name
            summary
          }
        }
      }
    }
  `)

  // Set these values by editing "siteMetadata" in gatsby-config.js

  return (
    <div className="bio">
      <p>
        Welcome to the DiMeN DTP Data Treasure Hunt! Below are a set of
        challenges you will need to complete as a group. When you complete a
        challenge, you will need to submit your answer to the front of the room
        to one of the helpers, who will keep track of your team's score. The
        challenges are labelled with how many points they are worth - the
        high-scoring challenges tend to be harder, and you might need to find
        creative ways to solve them. Good luck!
      </p>
    </div>
  )
}

export default Bio
