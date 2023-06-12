document.addEventListener("DOMContentLoaded",
  function ()
  {
    /*
    Start this off by checking if the make-post-button exists.
    That is; is a user signed in? Getting the Django user in JavaScript is a bit
    complicated, so this effectively checks if the button is created in the index.html
    template, which would confirm that a user is, indeed, signed in.
    */
    const make_post_button = document.querySelector("#make-post");
    /*
    If the button exists, attach an event listener to it. The button will unhide
    the post-form, and enable the post and cancel buttons on the form.
    The rest of it is handled by Django ORM, as the submit button on the template
    has a method of POST and a URL to the index view, where the post will be
    created. The Django form that is rendered has client side validation, so is protected
    from making an empty post because the form fields are REQUIRED.
    */
    if (make_post_button !== null)
    {
      make_post_button.addEventListener("click",
        function ()
        {
            document.querySelector("#make-post-div").hidden = true;
            document.querySelector("#make-post-form").hidden = false;
            document.querySelector("#cancel").addEventListener("click",
              function ()
              {
                document.querySelector("#make-post-div").hidden = false;
                document.querySelector("#make-post-form").hidden = true;
              }
            );
        }
      );
    };
  }
);

/*
An async function that puts a like from the current user to the identified post
with a PUT fetch request to the put_like view in Django.
The csrf_token appears to work like this, after a lot of tinkering, therefore
it eliminates the need for @csrf_exempt in views, which I feel much better about.
As before, I prefer making async functions rather than the chaining method. I do get
what chaining is doing, with "promises" and that, but it seems more unreadable and
rather cumbersome, which appears to defeat its very own purpose. Async functions are
perfectly good, and more than adequately suited to handling fetch requests.
*/
async function put_like(post_id, csrf_token)
{
  /*
  This business with the AbortController and Timeout function is a
  probably a very good idea. It will stop the function from hanging if it
  doesn't find what it is expecting.
  Async or Promises are kind of two faced, they can go wrong but not say
  anything about it. Therefore, those catch and if status.ok conditionals are
  rather important, even when the are merely printing the error to console,
  or uncaughts could start spilling around the browser, which I wager is not good.
  */
  //console.log("In Put Like");
  const cPutController = new AbortController();
  const fPutTimeout = setTimeout(
    function ()
    {
      cPutController.abort();
    },
    7000
  );

  const put_url = "like/" + post_id;
  try
  {
      const response = await fetch(put_url,
        {
          method: "PUT",
          headers: {
            "X-CSRFToken": csrf_token
          },
          signal: cPutController.signal
        }
      );
      if (response.ok)
      {
        //console.log("Okay");
        get_like(post_id);
      }
      else
      {
        console.log(`Error: ${response.status}`);
      };
  }
  catch (error)
  {
    console.log(`Error: ${error.name}`);
  }
  finally
  {
    clearTimeout(fPutTimeout);
  };
  return false;
}

/*
Separated async function that gets the liked post numbers with a GET fetch and
updates the count on the index.html page. Originally, this was neseted inside the
put_like function, but it was confusing to read, so it was removed and placed here.
There is a new get_likes function in the Django views, now, to accomodate it.
Better modularity, the function might even be useful for other things, further along.
Who knows?
*/
async function get_like(post_id)
{
  const cGetController = new AbortController();
  const fGetTimeout = setTimeout(
    function ()
    {
      cGetController.abort();
    },
    7000
  );

  const get_url = "getlikes/" + post_id;
  try
  {
    const like_response = await fetch(get_url,
      {
        method: "GET",
        signal: cGetController.signal
      }
    );
    if (like_response.ok)
    {
      // console.log("Got it");
      const likes = await like_response.json();
      const display_div = "#like-count" + post_id;
      document.querySelector(display_div).innerHTML = likes["like_count"];
    }
    else
    {
      // console.log("Not Got it");
      console.log(`Error: ${like_response.status}`);
    };
  }
  catch (error)
  {
    console.log(`Error: ${error.name}`);
  }
  finally
  {
    clearTimeout(fGetTimeout);
  };
  return false;
}


function do_edit(post_id)
{
  //console.log(post_id);
  //console.log(csrf_token);

  const text_area_id = "#text" + post_id;
  const edit_btn_id = "#edit-btn" + post_id;
  const save_btn_id = "#save-btn" + post_id;
  const text_area = document.querySelector(text_area_id);
  const edit_btn = document.querySelector(edit_btn_id);
  const save_btn = document.querySelector(save_btn_id);
  // const control_text = text_area.innerHTML;
  // console.log(control_text);

  text_area.disabled = false;
  text_area.setSelectionRange(0, text_area.value.length);
  text_area.focus();

  edit_btn.hidden = true;
  save_btn.hidden = false;
};

/*
Once the Save edit button is enabled and clicked, this is the function
that will replace the text in the Django data base with the new text,
using a fetch PUT request. Note here, the text is obtained from the
textarea the moment the button is clicked (its value), and that is stored
in the dict-like object in the fetch body, JSON stringified.
The csrf_token is also passed, in headers.
*/
async function put_edit(post_id, user_id, csrf_token)
{
  console.log(user_id);
  const text_area_id = "#text" + post_id;
  const new_text = document.querySelector(text_area_id).value;

  const cEditController = new AbortController();
  const fEditTimeout = setTimeout(
    function ()
    {
      cEditController.abort();
    },
    7000
  );

  const edit_url = "putedit/" + post_id;

  try
  {
    const edit_response = await fetch(edit_url,
      {
        method: "PUT",
        headers: {
          "X-CSRFToken": csrf_token
        },
        body: await JSON.stringify(
          {
            "new_text": new_text,
            "current_user": user_id
          }
        ),
        signal: cEditController.signal
      }
    );
    if (edit_response.ok)
    {
      console.log("Okay");
      /*
      HERE. If the response status was OK, then the program should
      update the edit date on the HTML web page. This is the place where
      that should be done. The post_id is already local in this function,
      so a new fetch can be done from here. Just to show that I do understand
      the "promise" way, and am not deliberately avoiding it with asyncs,
      I will use it once, right here...
      */

      const date_url = "geteditdate/" + post_id;

      fetch(date_url, {method: "GET"})
      .then(response => response.json())
      .then(
          function (data)
          {
            const edit_date = data["edit_date"];
            const div_element = document.querySelector(`#edited${post_id}`);
            div_element.innerHTML = "";
            const inner_element = document.createElement("h6");
            inner_element.innerHTML = `<i>Edited: ${edit_date}</i>`;
            div_element.appendChild(inner_element);
            /*
            // For reference, some of the stuff explored to get this working.
            // It was a lot easier, in the end.
            const edit_date = data["edit_date"]
            const last_id = "#last-edit" + post_id;
            const last_edit = document.querySelector(last_id);
            if (last_edit === null)
            {
              const first_id = "#first-edit" + post_id;
              const first_edit = document.querySelector(first_id);
              const element = document.createElement("h6");
              element.setAttribute("id", `inner-first-edit${post_id}`);
              element.innerHTML = `<i>Edited: ${edit_date}</i>`;
              first_edit.appendChild(element);
            }
            else if (last_edit === null && document.querySelector("#inner-first-edit" + post_id) !== null)
            {
              document.querySelector("#inner-first-edit" + post_id).innerHTML = `<i>Edited: ${edit_date}</i>`;
            }
            else // This, if the last-edit exists...
            {
              last_edit.innerHTML = `<i>Edited: ${edit_date}</i>`;
            };
            */
          }
        )
        .catch(error => console.log(error));
        // Satisfactory, I guess. It works.
    }
    else
    {
      console.log(`Error: ${edit_response.status}`);
    };
  }
  catch (error)
  {
    console.log(`Error: ${error.name}`);
  }
  finally
  {
    clearTimeout(fEditTimeout);
    /*
    No matter what happens, reset the edit button back to the page
    and disable the text edit window.
    */
    const text_area_id = "#text" + post_id;
    const edit_btn_id = "#edit-btn" + post_id;
    const save_btn_id = "#save-btn" + post_id;
    const edit_btn = document.querySelector(edit_btn_id);
    const save_btn = document.querySelector(save_btn_id);
    const text_area = document.querySelector(text_area_id);
    text_area.disabled = true;
    text_area.setSelectionRange(0, 0);
    edit_btn.hidden = false;
    save_btn.hidden = true;
    /*
    And finally, finally, the edit date should appear without having to do
    a page refresh. This can be accomplished with some more fetch stuff.
    The post_id is already present, so there should be no trouble getting this
    info from the database.
    In fact, a better place to do this is if the response status is ok, as
    the program COULD end up in "finally" even if the PUT fails.
    So, scroll back up to that...
    Done, here.
    */
  };
};

/*
DEFUNCT.
function restore_edit_btn(edit_btn, text_area)
{
  edit_btn.value = "Edit";
  edit_btn.className = "lsblue";
  text_area.disabled = true;
  text_area.setSelectionRange(0, 0);
};
*/
