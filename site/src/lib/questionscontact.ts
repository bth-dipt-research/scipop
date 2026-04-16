export function getQuestionText(name :string, email :string) :string {
  return `Questions regarding the research presented on this page? Contact <a href=mailto:${email}>${name}</a>.`
}
