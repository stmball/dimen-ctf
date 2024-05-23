import * as React from "react"

import { Link } from "gatsby"

function ChallengeCell({ post }) {
  return (
    <Link className="cell" to={post.fields.slug} itemProp="url">
      <strong>{post.frontmatter.title}</strong>
      {post.frontmatter.points}
    </Link>
  )
}

export default function ChallengeGrid({ posts }) {
  return (
    <div id="challenge-grid">
      {posts.map((post, idx) => {
        console.log(post)
        return <ChallengeCell key={idx} post={post} />
      })}
    </div>
  )
}
