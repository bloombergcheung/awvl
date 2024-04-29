var vm = new Vue({
    el: '#app',
    // 修改Vue变量的读取语法，避免和django模板语法冲突
    delimiters: ['[[', ']]'],
    data: {
        host,
        show_menu:false,
        username:'',
        is_login:false,
        email_address:'',
        user_desc: '',
        full_name:'',
        IP_address:'',
        Team_name:'',
        addhtml: false,
        container_card_next: '',

    },
    mounted(){
        this.username=getCookie('username');
        this.is_login=getCookie('is_login');
    },
  methods:{
      left_card(){
        this.container_card_next = 'left';
        setTimeout(() => {
          this.addhtml = true;
          }, 1000);
      },
      center_card(){
        this.addhtml = false;
        this.container_card_next = '';
      },
      close_right(){
        this.center_card();
      },
      preventDefault(event) {
        event.preventDefault();
      },
    },
    directives:{
      addhtml(element,binding){
        const get_index = binding.value;

        if(get_index === false){}
        else {
          // element.innerHTML="<div class='new_box'> </div>";
        }
      }
    }


});
