const readMemo = async () => {
  const res = await fetch("/memos");
  const jsonRes = await res.json();
  const ul = document.querySelector("#memo-ul");
  ul.innerHTML = "";
  jsonRes.forEach(displayMemo);
};

const editMemo = async (event) => {
  const id = event.target.dataset.id;
  const editInput = prompt("수정할 값을 입력하세요");
  const res = await fetch(`/memos/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
      content: editInput,
    }),
  });
  readMemo();
};

const deleteMemo = async (event) => {
  const id = event.target.dataset.id;
  const res = await fetch(`/memos/${id}`, {
    method: "DELETE",
  });
  console.log(id);
  readMemo();
};

const displayMemo = (memo) => {
  const ul = document.querySelector("#memo-ul");

  const li = document.createElement("li");
  li.innerText = `${memo.content}`;

  const editBtn = document.createElement("button");
  editBtn.innerText = "edit";
  editBtn.addEventListener("click", editMemo);
  editBtn.dataset.id = memo.id;

  const delBtn = document.createElement("button");
  delBtn.innerText = "delete";
  delBtn.addEventListener("click", deleteMemo);
  delBtn.dataset.id = memo.id;

  ul.appendChild(li);
  li.appendChild(editBtn);
  li.appendChild(delBtn);
};

const createMemo = async (title, content) => {
  const currentDate = new Date();
  const formattedDate = currentDate.toISOString().split("T")[0];
  console.log(formattedDate);
  console.log(title, content);
  const res = await fetch("/memos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: new Date().getTime(),
      title: title,
      content: content,
      createdAt: formattedDate,
    }),
  });
  const jsonRes = await res.json();
  console.log("[서버] 메모 생성 요청: ", jsonRes);
  readMemo();
};

const handleSubmit = (event) => {
  event.preventDefault();
  const input = document.querySelector("#memo-input");
  const content = input.value;
  const title = document.querySelector("#memo-title");
  console.log("title:", title.value, "content:", content);
  createMemo(title.value, content);
  input.value = "";
  title.value = "";
};

const form = document.querySelector("#memo-form");
form.addEventListener("submit", handleSubmit);

readMemo();
