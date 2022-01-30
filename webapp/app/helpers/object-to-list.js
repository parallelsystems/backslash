import { helper } from '@ember/component/helper';

export function objectToList(params /*, hash*/) {
    let object = params[0];
    let list = []
    for (const property in object){
        // this is a hack for UP Demo remove this
        if (property != "slash::tags"){
            list.push({key: property, value: JSON.stringify(object[property])});
        }
    }
    return list;
}

export default helper(objectToList);
