window.addEventListener("load", function() {
    (function ($) {
        $(function () {

            function toggleVerified(value, index) {
                let textBlock = $(`#blocks-${index}-text-group`)
                let imageBlock = $(`#blocks-${index}-image-group`)
                let videoBlock = $(`#blocks-${index}-video-group`)
                let questionBlock = $(`#blocks-${index}-question-group`)
                switch (value) {
                    case 'Text': {
                        textBlock.find('> div > fieldset > table > tbody > tr:last-child > td > a ').parent().remove()
                        textBlock.show()
                        imageBlock.hide()
                        videoBlock.hide()
                        questionBlock.hide()
                        break;
                    }
                    case 'Image': {
                        imageBlock.find('> div > fieldset > table > tbody > tr:last-child > td > a ').parent().remove()
                        textBlock.hide()
                        imageBlock.show()
                        videoBlock.hide()
                        questionBlock.hide()
                        break;
                    }
                    case 'Video': {
                        videoBlock.find('> div > fieldset > table > tbody > tr:last-child > td > a ').parent().remove()
                        textBlock.hide()
                        imageBlock.hide()
                        videoBlock.show()
                        questionBlock.hide()
                        break;
                    }
                    case 'Question': {
                        questionBlock.find('> div > fieldset > table > tbody > tr:last-child > td > a ').parent().remove()
                        textBlock.hide()
                        imageBlock.hide()
                        videoBlock.hide()
                        questionBlock.show()
                        break;
                    }
                }
            }

            function checkBlocks() {
                let selectFields = $('*[id*=type_of_block]')
                let index = 0
                for (let selectField of selectFields) {
                    toggleVerified(selectField.value, index)
                    index++
                }
            }

            let blocks = $('#blocks-group')
            let add_row = $('.add-row')
            checkBlocks()
            blocks.change(function () {
                checkBlocks()
            })
            add_row.click(function () {
                checkBlocks()
            })
            $("input[name='_continue'], input[name='_addanother'], input[name='_save']").click(function(e){
                e.preventDefault();
                var form_valid = false;

                var blocks_id_exists = 0
                var blocks_id_text_flag = true
                while(blocks_id_text_flag){
                    var blocks_text = $("#id_blocks-"+blocks_id_exists+"-text-0-text")
                    if(blocks_text.get(0) !== undefined){
                        if (blocks_text.val().length > 0) {
                            blocks_text.prev('ul').remove()
                            blocks_text.css('border', '1px solid var(--border-color)')
                            form_valid = true
                        } else {
                            blocks_text.prev('ul').remove()
                            blocks_text.before('<ul class="errorlist" style="background: white;"><li>This field is required.</li></ul>')
                            blocks_text.css('border', '1px solid var(--error-fg)')
                            form_valid = false
                        }
                        blocks_id_exists++;
                    } else {
                        blocks_id_text_flag = false
                    }
                }

                var image_id_exists = 0
                var image_id_flag = true
                while(image_id_flag){
                    var blocks_image = $("#id_blocks-"+image_id_exists+"-image-0-image")
                    if(blocks_image.get(0) !== undefined){
                        if (blocks_image.val().length > 0) {
                            blocks_image.prev('ul').remove()
                            blocks_image.css('border', '1px solid var(--border-color)')
                            form_valid = true
                        } else {
                            blocks_image.prev('ul').remove()
                            blocks_image.before('<ul class="errorlist" style="background: white;"><li>This field is required.</li></ul>')
                            blocks_image.css('border', '1px solid var(--error-fg)')
                            form_valid = false
                        }
                        image_id_exists++;
                    } else {
                        image_id_flag = false
                    }
                }

                var video_id_exists = 0
                var video_id_flag = true
                while(video_id_flag){
                    var blocks_video = $("#id_blocks-"+video_id_exists+"-video-0-video")
                    if(blocks_video.get(0) !== undefined){
                        if (blocks_video.val().length > 0) {
                            blocks_video.prev('ul').remove()
                            blocks_video.css('border', '1px solid var(--border-color)')
                            form_valid = true
                        } else {
                            blocks_video.prev('ul').remove()
                            blocks_video.before('<ul class="errorlist" style="background: white;"><li>This field is required.</li></ul>')
                            blocks_video.css('border', '1px solid var(--error-fg)')
                            form_valid = false
                        }
                        video_id_exists++;
                    } else {
                        video_id_flag = false
                    }
                }

                var question_id_exists = 0
                var question_id_flag = true
                while(question_id_flag){
                    var blocks_question = $("#id_blocks-"+question_id_exists+"-question-0-text")
                    if(blocks_question.get(0) !== undefined){
                        if (blocks_question.val().length > 0) {
                            blocks_question.prev('ul').remove()
                            blocks_question.css('border', '1px solid var(--border-color)')
                            form_valid = true
                        } else {
                            blocks_question.prev('ul').remove()
                            blocks_question.before('<ul class="errorlist" style="background: white;"><li>This field is required.</li></ul>')
                            blocks_question.css('border', '1px solid var(--error-fg)')
                            form_valid = false
                        }
                        var question_id_flag_text_tip = true
                        var question_id_exists_text_tip = 0
                        while(question_id_flag_text_tip){
                            var blocks_question_text = $("#id_blocks-"+question_id_exists+"-question-0-options-"+question_id_exists_text_tip+"-text")
                            var blocks_question_tip = $("#id_blocks-"+question_id_exists+"-question-0-options-"+question_id_exists_text_tip+"-tip")
                            if(blocks_question_text.get(0) !== undefined) {
                                if (blocks_question_text.val().length > 0) {
                                    blocks_question_text.prev('ul').remove()
                                    blocks_question_text.css('border', '1px solid var(--border-color)')
                                    form_valid = true
                                } else {
                                    blocks_question_text.prev('ul').remove()
                                    blocks_question_text.before('<ul class="errorlist" style="background: white;"><li>This field is required.</li></ul>')
                                    blocks_question_text.css('border', '1px solid var(--error-fg)')
                                    form_valid = false
                                }
                                if (blocks_question_tip.val().length > 0) {
                                    blocks_question_tip.prev('ul').remove()
                                    blocks_question_tip.css('border', '1px solid var(--border-color)')
                                    form_valid = true
                                } else {
                                    blocks_question_tip.prev('ul').remove()
                                    blocks_question_tip.before('<ul class="errorlist" style="background: white;"><li>This field is required.</li></ul>')
                                    blocks_question_tip.css('border', '1px solid var(--error-fg)')
                                    form_valid = false
                                }
                                question_id_exists_text_tip++;
                            } else {
                                question_id_flag_text_tip = false
                            }
                        }
                        question_id_exists++;
                    } else {
                        question_id_flag = false
                    }
                }


                if (form_valid){
                    $("form").submit()
                }
            });
        });
    })(django.jQuery);
})

