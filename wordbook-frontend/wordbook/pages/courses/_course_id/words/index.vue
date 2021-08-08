<template>
    <div class="">

        <v-data-table
            :headers="headers"
            :items="words"
            :options.sync="options"
            :server-items-length="serverItemsLength"
            :loading="loading"
            class="elevation-1"
        >

        <template #top>
            <v-toolbar flat>
                <v-toolbar-title>Wordlist</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>
                <v-btn color="primary" dark class="mb-2 mr-2" @click="goToCourses">
                    Back To Courses
                </v-btn>
                <v-btn color="primary" dark class="mb-2 mr-2" @click="goToPractice">
                    Practice
                </v-btn>
                <v-dialog v-model="dialog" max-width="500px">
                    <template #activator="{ on, attrs }">
                    <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                        New Item
                    </v-btn>
                    </template>
                <v-card>
                    <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field v-model="editedItem.word" label="word"></v-text-field>
                                    <v-text-field v-model="editedItem.pronunciation" label="pronunciation"></v-text-field>
                                    <v-textarea v-model="editedItem.hint" label="hint"></v-textarea>
                                    <v-textarea v-model="editedItem.description" label="description"></v-textarea>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-text>

                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">
                        Cancel
                    </v-btn>
                    <v-btn color="blue darken-1" text @click="save">
                        Save
                    </v-btn>
                    </v-card-actions>
                </v-card>
                </v-dialog>
                <v-dialog v-model="dialogDelete" max-width="500px">
                    <v-card>
                        <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
                        <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
                        <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
                        <v-spacer></v-spacer>
                        </v-card-actions>
                    </v-card>
                </v-dialog>
            </v-toolbar>
        </template>

        <template #item.actions="{item}">
        <v-icon small class="mr-2" @click="editItem(item)">
            mdi-pencil
        </v-icon>
        <v-icon small @click="deleteItem(item)">
            mdi-delete
        </v-icon>
        </template>

        </v-data-table>
    </div>
</template>

<script>
export default {
    name: "WordsComponent",
    middleware: 'auth',
    data() {
        return {
            words: [],
            courseId: this.$route.params.course_id,
            loading: true,
            serverItemsLength: 1,
            options: {
                page: 1,
                itemsPerPage: 10,
                sortBy:['id'],
                sortDesc:[true],
            },
            headers: [
                { text: "word", value: "word" },
                { text: "description", value: "description" },
                { text: "pronunciation", value: "pronunciation" },
                { text: "hint", value: "hint" },
                { text: 'Actions', value: 'actions', sortable: false },
            ],
            dialog: false,
            dialogDelete: false,
            editedIndex: -1,
            editedItem: {
                word: '',
                description: '',
                hint: '',
                pronunciation: '',
            },
            defaultItem: {
                word: '',
                description: '',
                hint: '',
                pronunciation: '',
            },

        };
    },
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },
    watch: {
        options: {
            handler() {
                this.$nextTick(function () {
                    this.readDataFromAPI();
                });
            },
        },
        dialog (val) {
            val || this.close()
        },
        dialogDelete (val) {
            val || this.closeDelete()
        },
        deep: true,
    },
    mounted() {
        this.readDataFromAPI();
    },
    methods: {
        readDataFromAPI() {
            this.loading = true;
            const sortBy = this.options.sortBy[0];
            const sortDesc = this.options.sortDesc[0];
            this.$axios.get(
                `/courses/${this.courseId}/words/`,
                {
                    params:{
                        'page': this.options.page,
                        'count': this.options.itemsPerPage,
                        'ordering': (sortDesc ? '':'-') + sortBy
                    }
                }
            ).then((response) => {
                this.loading = false;
                this.words = response.data.data;
                this.serverItemsLength = response.data.total;
            });
        },
        updateDataToAPI(itemToUpdate) {
            this.loading = true;
            this.$axios.patch(
                `/courses/${this.courseId}/words/${itemToUpdate.id}/`,
                {'word': itemToUpdate.word, 'description': itemToUpdate.description, 'pronunciation': itemToUpdate.pronunciation, 'hint': itemToUpdate.hint}
            ).then((response) => {
                this.loading = false;
                return true;
            }).catch((response) => {
                this.loading = false;
                return false;
            });
        },
        async postDataToAPI(itemToUpdate) {
            this.loading = true;
            const response = await this.$axios.post(
                `/courses/${this.courseId}/words/`,
                {'word': itemToUpdate.word, 'description': itemToUpdate.description, 'pronunciation': itemToUpdate.pronunciation, 'hint': itemToUpdate.hint}
            )
            this.loading = false;
            return response.data;
        },
        deleteDataToAPI(itemToUpdate) {
            this.loading = true;
            this.$axios.delete(
                `/courses/${this.courseId}/words/${itemToUpdate.id}/`,
            ).then((response) => {
                this.loading = false;
                return true;
            }).catch((response) => {
                this.loading = false;
                return false;
            });
        },
        editItem (item) {
            this.editedIndex = this.words.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialog = true;
        },
        deleteItem (item) {
            this.editedIndex = this.words.indexOf(item);
            this.editedItem = Object.assign({}, item);
            this.dialogDelete = true;
        },
        deleteItemConfirm () {
            this.deleteDataToAPI(this.editedItem)
            this.words.splice(this.editedIndex, 1);
            this.closeDelete();
        },
        close () {
            this.dialog = false
            this.$nextTick(() => {
                this.editedItem = Object.assign({}, this.defaultItem);
                this.editedIndex = -1;
            })
        },
        closeDelete () {
            this.dialogDelete = false
            this.$nextTick(() => {
                this.editedIndex = -1;
                this.readDataFromAPI();
            })
        },
        save () {
            if (this.editedIndex > -1) {
                this.updateDataToAPI(this.editedItem)
                Object.assign(this.words[this.editedIndex] , this.editedItem);
            } else {
                this.$nextTick(function () {
                    this.postDataToAPI(this.editedItem).then((createdItem) => {                
                        this.readDataFromAPI();
                    })
                })
            }
            this.close()
        },
        goToCourses (){
            this.$router.push('/courses/');
        },
        goToPractice (row){
            this.$router.push(`/courses/${this.courseId}/words/practice/`);
        },
    },
};
</script>
